import os 
import json

with open(os.path.join("src", "mapworld", "categories.json"), 'r') as f:
    json_data = json.load(f)

with open(os.path.join("src", "mapworld", "mapping.json"), 'r') as f:
    mapping_data = json.load(f)


updated_data = {}

for k in json_data.keys():
    new_list = []
    for val in json_data[k]:
        new_list.append(mapping_data[val])
    
    updated_data[k] = new_list

with open(os.path.join("src", "mapworld", "categories.json"), 'w') as f:
    json.dump(updated_data, f, indent=4)