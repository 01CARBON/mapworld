import json
import os
import requests
from tqdm import tqdm

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open(os.path.join("src", "mapworld", "images.json"), 'r') as f:
    image_data = json.load(f)

for k in image_data.keys():
    images = image_data[k]
    for img in tqdm(images, desc=f"Testimg images for {k}", leave=False):
        if requests.get(img, verify=False).status_code != 200:
            raise RuntimeError(f"Unable to fetch image - {img}. Try again when the server is running, or provide a json file containing local image paths")
