#!/bin/python
import subprocess
import sys
import os

# To run this script, use the following syntax:
#   python testWDLTasks.py /absolute/path/to/wdl_tasks_dir /absolute/path/to/wdltool.jar 
# This script will print out the name of the file as it checks the file.
# If no errors are found in that file, there will be an empty line under the filename.
# If errors are found, the error message will be output under the filename.
# This script should be run prior to uploading any auto-generated WDL tasks to the repository.

directory = sys.argv[1]
wdltool = sys.argv[2]

dirWDLs = os.listdir(directory)

for a in range(0,len(dirWDLs)):
    if(".wdl" in dirWDLs[a]):
        print(dirWDLs[a])
        subprocess.call("java -jar " + wdltool + " validate " + directory + "/" + dirWDLs[a], shell=True)
