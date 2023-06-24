import requests
import time
import csv
import re

response = requests.get('https://api.tosdr.org/all-services/v1/')
services = response.json()["parameters"]["services"]

ids=[]
for service in services:
    ids.append(service["id"])

print(f"{len(ids)} services")

rows=[]
url="https://api.tosdr.org/service/v1/"

for n, id in enumerate(ids):
    
    response = requests.get(url, params={"service":id})
    while response.status_code != 200:
        print("waiting for 200 status...")
        time.sleep(60)
        response = requests.get(url, params={"service":id})

    try:
        points = response.json()["parameters"]["points"]
    except:
        print(f"{n} Error! skipping service {id}")
        continue

    print(f"{n} scraping service {id}")
    for point in points:
        if point["status"]=="approved" and point["quoteText"] is not None:
            text = point["quoteText"]
            text = re.sub("\<.*?\>",'',text) # removing tags
            text = '"'+text+'"'
            case = point["case_id"]
            rows.append([text, case])

with open('tos.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"]) # headers
    writer.writerows(rows)

print("All Done!") 