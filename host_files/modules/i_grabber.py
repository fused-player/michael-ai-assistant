import os
import requests 
import sys
import subprocess
import time
import random

API_KEY = ''
CX = ''
with open("api.d","w+") as f:
	apis = f.readlines()
	API_KEY = apis[1]
	CX = apis[2]
	host_name = apis[3]

SHARED_D_G = f"/home/{host_name}/.michael"

url = "https://www.googleapis.com/customsearch/v1"
choose = sys.argv[1]
query = sys.argv[2]


params = {
	'q': query,
	'cx': CX,
	'key': API_KEY,
	'searchType': 'Image',
	'num': 6

}


response = requests.get(url,params=params)
data = response.json()

if 'items' in data:
	image_urls = [item['link'] for item in data['items']]
	print(image_urls)

else :
	print("NO images found")

print(f"**************{query}****************")
if choose == 'few':
	for index,image in enumerate(image_urls):
		subprocess.run(f"curl -o {os.path.join(SHARED_D_G,f"{query}_{index}.jpg")} {image}",shell=True)
elif choose == 'one':
	subprocess.run(f"curl -o {os.path.join(SHARED_D_G,f"{query}.jpg")} {image_urls[random.randrange(0,2)]}",shell=True)
