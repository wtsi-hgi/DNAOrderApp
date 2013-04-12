import json

# read in data from file
data = open("phenodb_data_1_fixed.json").read()

# it is set to json string format, members are tuple; encode into json
data_json_string = json.dumps(data, indent=2)

# decode into python format, now it is a list
data_python_string = json.loads(data_json_string)
