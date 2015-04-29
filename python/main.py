import binding
import engine
import argparse
import json

parser = argparse.ArgumentParser(description='Common Workflow Language DSL Reference Implementation')
parser.add_argument('cwl_file', help='Path to CWL file')
parser.add_argument('--inputs', help='Path to JSON file to define inputs')
cli = parser.parse_args()

inputs = None
if cli.inputs:
    with open(cli.inputs) as fp:
        inputs = json.loads(fp.read())

try:
    engine.run(cli.cwl_file, inputs)
except engine.MissingInputsException as error:
    print("Your workflow cannot be run because it is missing some inputs!")
    if cli.inputs:
        print("Add the following keys to your {} file and try again:".format(cli.inputs))
    else:
        print("Use the template below to specify the inputs.  Keep the keys as-is and change the values to match the type specified")
        print("Then, pass this file in as the --inputs option:\n")
    print(json.dumps(error.missing, indent=4))
