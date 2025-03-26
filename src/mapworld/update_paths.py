import requests
import certifi
import os
import json

base_url = "https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/"

# response = requests.get(base_url, verify=False)

major_categories = [
    'cultural',
    'home_or_hotel',
    'industrial',
    'nature_landscape',
    'shopping_and_dining',
    'sports_and_leisure',
    'transportation',
    'unclassified',
    'urban',
    'work_place'
]

def find_exact_path(category):
    for m in major_categories:
        possible_path = os.path.join(base_url, m, category)
        if requests.get(possible_path, verify=False).status_code == 200:
            return possible_path
    
    return None


with open(os.path.join("src", "mapworld", "img_instances.json"), 'r') as f:
    json_data = json.load(f)

updated_image_paths = {}
updated_mapping = {}

failed_keys = []
for key in json_data.keys():
    splits = key.split('/')
    if len(splits) == 2:
        updated_key = splits[-1]
    elif len(splits) == 3:
        updated_key = splits[1] + "__" + splits[2]
    else:
        print(f"CHECK - {splits}")

    updated_mapping[key] = updated_key

    folder_path = find_exact_path(updated_key)
    if not folder_path:
        raise RuntimeError(f"Path finding failed for - {updated_key}. Find path manually")

    images = []
    for img in json_data[key]:
        rel_img_pth = img.split('/')[-1]
        image_server_path = os.path.join(folder_path, rel_img_pth)
        images.append(image_server_path)

    updated_image_paths[updated_key]  = images


with open(os.path.join("src", "mapworld", "images.json"), 'w') as f:
    json.dump(updated_image_paths, f, indent=4)

with open(os.path.join("src", "mapworld", "mapping.json"), 'w') as f:
    json.dump(updated_mapping, f, indent=4)