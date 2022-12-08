import requests
import json
from bs4 import BeautifulSoup
from bs2json import bs2json


file = open("buzzfeed.json")
converter = bs2json()

data = json.load(file)

address = []
temp = []


for i in range(17, 18):
    address.append(data[i]["url"])

for i in address:
    page = requests.get(i)
    soup = BeautifulSoup(page.text, 'html.parser')
    temp.append(soup.find_all("button"))
    # print(soup.find_all('a').get_text())

for i in temp:
    for y in i:
        print(y.get_text())
# json = converter.convertAll(temp,join=True)
# json.dumps(soup)
# print(json.dumps(temp))
