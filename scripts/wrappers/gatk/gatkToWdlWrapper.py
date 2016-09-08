#!/bin/python
import json
import sys
import datetime
import os

#The following python script is designed to take in a directory of json files containing GATK tools,
# and output a WDL task file for each one.

def getWdlType(jsonType):
    if(jsonType.lower() == "double"):
        return "Float"
    elif(jsonType.lower() == "integer" or jsonType.lower() == "int"):
        return "Int"
    elif(jsonType.lower() == "boolean"):
        return "Boolean"
    elif(jsonType.lower() == "file"):
        return "File"
    elif("list" in jsonType.lower()):
        substring = jsonType[jsonType.find("[")+1:len(jsonType)-1]
        return "Array[" + getWdlType(substring) + "]"
    else:
        return "String"

def getArgIndexByName(nameStr, args):
    for x in range(0,len(args)):
        if  args[x]["name"].lower() == nameStr.lower():
            return x
    return -1

def checkName(nameStr):
    index = nameStr.find(":")
    if nameStr =="input":
        return checkName("task_" + nameStr)
    elif index>0:
        return checkName(nameStr[0:index] + nameStr[index+1:])
    else:
        return nameStr

def checkQuotes(myStr):
    index = myStr.find("\"")
    if index < 0:
        return myStr
    else:
        return checkQuotes(myStr[0:index]+myStr[index+1:])
        
#collect inputs
directory = sys.argv[1]
version = sys.argv[2]

dirFiles = os.listdir(directory)
engineJson = directory + "/engine_args_per_tool.json"
cmdJson = directory + "/org_broadinstitute_gatk_engine_CommandLineGATK.php.json"

#open files and grab data
with open(engineJson) as engineFile:
    engineData = json.load(engineFile)
with open(cmdJson) as cmdFile:
    cmdData = json.load(cmdFile)

dirJsons = []
for a in range(0, len(dirFiles)):
    if ".json" in dirFiles[a] and "gatk_tools" in dirFiles[a]:
        dirJsons.append(directory + "/" + dirFiles[a])

#iterate over each file in the directory of jsons
#TODO: change 3 to len(dirJsons)
for a in range(0,len(dirJsons)):
    toolJson = dirJsons[a]

    #open the tool file, and load the data
    with open(toolJson) as toolFile: 
        toolData = json.load(toolFile)

    #grab frequently used sections from toolData for easier access
    toolName = toolData["name"]
    toolArgs = toolData["arguments"]
    cmdArgs = cmdData["arguments"]

    if("Tools" in toolData["group"]):
        #open the output file
        filename = directory + "/WDLTasks/" + toolName + "_" + version + ".wdl"
        wdlFile = open(filename, 'w')

        #parse the summary text to cut after \n
        cutIndex = toolData["summary"].find("\n")
        if cutIndex > 0:
            toolSummary = toolData["summary"][0:cutIndex]
        else:
            toolSummary = toolData["summary"]

        #Write header and declare task
        wdlFile.write("# --------------------------------------------------------------------------------------------\n" +
                      "# This " + toolName + " WDL task was generated on " + datetime.date.today().strftime("%m/%d/%y") +
                      " for use with GATK version " + version + "\n" +
                      "# For more information on using this wrapper, please see the WDL repository at \n" +
                      "# https://github.com/broadinstitute/wdl/tree/develop/scripts/wrappers/gatk/README.md\n" +
                      "# Task Summary: " + toolSummary + "\n" +
                      "# --------------------------------------------------------------------------------------------\n\n")
        wdlFile.write("task " + toolName + " { \n")

        #declare default inputs
        wdlFile.write("\tFile gatk\n" +
                      "\tFile ref\n" +
                      "\tFile refIndex\n" +
                      "\tFile refDict\n" +
                      "\tString ? userString #If a parameter you'd like to use is missing from this task, use this term to add your own string\n")

        #declare engine-level inputs
        if toolName in engineData.keys():
            for b in range(0,len(engineData[toolName])):
                if engineData[toolName][b][2].lower() == "required":
                    wdlFile.write("\t" + getWdlType(cmdArgs[getArgIndexByName(engineData[toolName][b][0], cmdArgs)]["type"]) +
                                  " " + checkName(engineData[toolName][b][0][2:]) + "\n")
                elif engineData[toolName][b][2].lower() == "optional":
                    wdlFile.write("\t" + getWdlType(cmdArgs[getArgIndexByName(engineData[toolName][b][0], cmdArgs)]["type"]) +
                                  " ? " + checkName(engineData[toolName][b][0][2:]) + "\n")
                else:
                    print("There was an error determining the optional status of an engine argument: Input received: "
                          + engineData[toolName][e][2] + " for the argument " + toolName + ": " + engineData[toolName][e][0])
                    
        #iterate through remaining inputs (non-defaults)
        for b in range(0,len(toolData["parallel"])):
            wdlFile.write("\tInt ? " + toolData["parallel"][b]["arg"][1:] + "Val\n")
        for b in range(0,len(toolArgs)):
            if toolArgs[b]["required"] == "yes":
                wdlFile.write("\t" + getWdlType(toolArgs[b]["type"]) + " " + checkName(toolArgs[b]["name"][2:]) + "\n") 
            elif toolArgs[b]["required"] == "no":
                wdlFile.write("\t" + getWdlType(toolArgs[b]["type"]) + " ? " + checkName(toolArgs[b]["name"][2:]) + "\n") 
            else:
                print("There was an error determining optional status of an argument. Input received: "
                      + toolArgs[b]["required"] + " for the argument " + toolArgs[b]["synonyms"])

        #write command
        wdlFile.write("\n\tcommand {\n" +
                      "\t\tjava -jar ${gatk} \\\n" +
                      "\t\t\t-T " + toolName + " \\\n" +
                      "\t\t\t-R ${ref} \\\n")

        #add additional engine-level arguments
        if toolName in engineData.keys():
            for b in range(0,len(engineData[toolName])):
                if engineData[toolName][b][2].lower() == "required":
                    wdlFile.write("\t\t\t" + engineData[toolName][b][0] + " ${" + checkName(engineData[toolName][b][0][2:]) + "} \\\n")
                elif engineData[toolName][b][2].lower() == "optional":
                    if engineData[toolName][b][1].lower() == "null":
                        wdlFile.write("\t\t\t${default=\"\" \"" + engineData[toolName][b][0] + " \" + " + checkName(engineData[toolName][b][0][2:]) +
                                      "} \\\n")
                    else:
                        wdlFile.write("\t\t\t" + engineData[toolName][b][0] + " ${default=\"" + checkQuotes(engineData[toolName][b][1]) + "\" " +
                                      checkName(engineData[toolName][b][0][2:]) + "} \\\n")
                else:
                    print("There was an error determining the optional status of an engine argument: Input received: " +
                          engineData[toolName][b][2] + " for the argument " + toolName + ": " + engineData[toolName][b][0])
                    

        #iterate through remaining options (non-defaults)
        for b in range(0,len(toolData["parallel"])):
            wdlFile.write("\t\t\t${default=\"\" \"" + toolData["parallel"][b]["arg"] + "\" + " + toolData["parallel"][b]["arg"][1:] + "Val} \\\n")                 
        for b in range(0,len(toolArgs)):
            if toolArgs[b]["required"] == "yes":
                wdlFile.write("\t\t\t" + toolArgs[b]["synonyms"] + " ${" + checkName(toolArgs[b]["name"][2:]) + "} \\\n") 
            elif toolArgs[b]["required"] == "no":
                if toolArgs[b]["defaultValue"] != "NA" and toolArgs[b]["defaultValue"] != "none" and toolArgs[b]["defaultValue"] != "[ ]":
                    if toolArgs[b]["synonyms"] != "NA":
                        wdlFile.write("\t\t\t" + toolArgs[b]["synonyms"] + " ${default=\"" + checkQuotes(toolArgs[b]["defaultValue"]) + "\" " +
                                  checkName(toolArgs[b]["name"][2:]) + "} \\\n")
                    else:
                        wdlFile.write("\t\t\t" + checkName(toolArgs[b]["name"][2:]) + " ${default=\"" + checkQuotes(toolArgs[b]["defaultValue"]) + "\" " +
                                  checkName(toolArgs[b]["name"][2:]) + "} \\\n")
                else:
                    if toolArgs[b]["synonyms"] != "NA":
                        wdlFile.write("\t\t\t${default=\"\" \"" + toolArgs[b]["synonyms"] + " \" + " + checkName(toolArgs[b]["name"][2:]) + "} \\\n")
                    else:
                        wdlFile.write("\t\t\t${default=\"\" \"" + checkName(toolArgs[b]["name"][2:]) + " \" + " + checkName(toolArgs[b]["name"][2:]) + "} \\\n")
            else:
                print("There was an error determining optional status of an argument. Input received: " +
                      toolArgs[b]["required"] + " for the argument " + toolArgs[b]["synonyms"])
        wdlFile.write("\t\t\t${default=\"\\n\" userString} \n" + 
                      "\t}\n")

        #write output
        wdlFile.write("\n\toutput {\n" +
                      "\t\t#To track additional outputs from your task, please manually add them below\n" +
                      "\t\tString taskOut = \"${out}\"\n" +
                      "\t}\n")

        #write runtime
        #TODO Replace docker image with GATK-specific one
        wdlFile.write("\n\truntime {\n" +
                      "\t\tdocker: \"broadinstitute/genomes-in-the-cloud:2.2.2-1466113830\"\n" +
                      "\t}\n")

        #write parameter_meta
        wdlFile.write("\n\tparameter_meta {\n" +
                      "\t\tgatk: \"Executable jar for the GenomeAnalysisTK\"\n" +
                      "\t\tref: \"fasta file of reference genome\"\n" +
                      "\t\trefIndex: \"Index file of reference genome\"\n" +
                      "\t\trefDict: \"dict file of reference genome\"\n" +
                      "\t\tuserString: \"An optional parameter which allows the user to specify additions to the command line at run time\"\n")
        for b in range(0,len(toolArgs)):
            wdlFile.write("\t\t" + checkName(toolArgs[b]["name"][2:]) + ": \"" + checkQuotes(toolArgs[b]["summary"]) + "\"\n")
        if toolName in engineData.keys():
            for b in range(0,len(engineData[toolName])):
                wdlFile.write("\t\t" + checkName(engineData[toolName][b][0][2:]) + ": \"" +
                              checkQuotes(cmdArgs[getArgIndexByName(engineData[toolName][b][0], cmdArgs)]["summary"]) + "\"\n" )
        wdlFile.write("\t}\n}")

        #close file
        wdlFile.close()
