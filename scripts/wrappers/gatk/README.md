###Introduction
In this directory, you will find 3 different types of files. 
- WDL task files (named using the format `ToolName_GATKVersion.wdl`) located under a folder named for their GATK version
- A python script for generating these WDL task files (`gatkToWdlWrapper.py`)
- A python script for validating the WDL task files (`testWDLTasks.py`)

###Using WDL task files
These task files are workflow-less. They contain only the task specified by the GATK tool they are named for. You can choose to either copy them into your workflow WDL, as is presented in our [WDL tutorials](https://software.broadinstitute.org/wdl/userguide/topic?name=wdl-tutorials), or you can import the task into your workflow file. To import a task, download the task script you would like to use, and save it in the same directory as your workflow WDL. Then, at the top of the file, you can import using the following syntax:
```
import ToolName_GATKVersion.wdl as toolName
```

To call an imported tool in your workflow, you can then use the following syntax:
```
call toolName.taskName{ inputs: ... }
```

For example, let's say you want to use VariantEval. You can use the task like so:
```
import VariantEval_3.6.wdl as variantEval
workflow wf {
  call variantEval.VariantEval{ inputs: ... }
}
```

These task files were generated to give you all possible parameters available to the tool itself. Any parameter marked with a `?` is denoted as optional. Optional parameters do not need to be specified if you do not wish to use them. If you do not specify a value for an optional parameter, the default value for it will be used, according to the default recommendations for the GATK tool itself. If the GATK tool has no default (such as in a case where you could choose to pass in a file or not), then the parameter will not be used at all in the final command. 

If you find there is a parameter you would like to use, and it has not been specified in the command as an option, you can use the variable called `userString`. There are many parameters, for example, available to all GATK tools via the [CommandLineGATK options](https://software.broadinstitute.org/gatk/documentation/tooldocs/org_broadinstitute_gatk_engine_CommandLineGATK.php), that do not make sense to use in a majority of cases. However, if you find there is a parameter you'd like to use, you can pass it in as a simple string, as you would type it into the command when running a GATK tool from the terminal.

These options are all designed so that you never need to edit the task file itself, simply import and use it immediately in your workflow. If you find any errors in using these WDL tasks, please report them to us on the [WDL forum](http://gatkforums.broadinstitute.org/wdl/categories/ask-the-wdl-team). You are also welcome to ask us any and all questions related to running GATK with WDL on that forum.

###Generating WDL task files
These instructions are intended primarily for internal use. In order to run this python script, you will need:
- `gatkToWdlWrapper.py`
- Python installed on your computer
- a folder of JSON files generated from GATK tools, including the JSON for CommandLineGATK
- a file titled `engine_args_per_tool.json` specific to the version of GATK you are generating the JSON files for (You can find one in the WDLTasks_3.6 subfolder)

Once you have all of the above requirements on your local machine, go into the directory containing all your JSON files and create a new folder titled `WDLTasks`. To run the script, open up your terminal and execute the command with the following syntax:

```
python gatkToWdlWrapper.py /absolute/path/to/directoryofJsons GATKVersion
```

The resulting WDL tasks will be output to the folder you just created, WDLTasks. You must test that these tasks are valid, using the test script next, prior to uploading.

###Testing WDL task files
This test script simply validates that the WDL tasks follow all WDL rules. They do not guarantee that the commands themselves are valid, but this test does offer a simple sanity check. To run this python script, you will need:
- `testWDLTasks.py`
- Python installed on your computer
- wdltool.jar
- the resulting WDL tasks from the previous section

Again, once you have all the above requirements on your local machine, run the script using the following syntax:

```
python testWDLTasks.py /absolute/path/to/WDLTasks /absolute/path/to/wdltool.jar
```

This will print out the name of the WDL task as it checks it. If an error in the script is found, it will output the error message below the name of the file it is associated with. If no error is found, a blank line will simply be output. All errors must be fixed prior to uploading the WDL tasks to this repository.
