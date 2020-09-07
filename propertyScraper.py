# this is a version of the program provided on this page
# https://www.promptcloud.com/blog/scraping-real-estate-data-from-zillow-using-python/
# To the existing code, I added some additional features such as ..
# I also created a for loop that goes through a column in a table consisting of url's
# without asking user for the input

import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import ast
import os
from urllib.request import Request, urlopen

# For ignoring SSL certificate errors

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = input("Enter Zillow House Listing Url- ")

url = "https://www.zillow.com/homedetails/715-10th-Ave-SE-Minneapolis-MN-55414/1921742_zpid/"

# Making the website believe that you are accessing it using a mozilla browser

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

# Creating a BeautifulSoup object of the html page for easy extraction of data.

soup = BeautifulSoup(webpage, 'html.parser')
html = soup.prettify('utf-8')
property_json = {}
property_json["Details_Broad"] = {}
property_json['Address'] = {}

# Extract Title of the property listing

for title in soup.findAll('title'):
    property_json['Title'] = title.text.strip()
    break

for meta in soup.findAll('meta', attrs={'name': 'description'}):
    property_json['Detail_Short'] = meta['content'].strip()

for div in soup.findAll('div', attrs={'class': 'character-count-truncated'}):
    property_json['Details_Broad']['Description'] = div.text.strip()


for (i, script) in enumerate(soup.findAll('script', attrs={'type': 'application/ld+json'})):
    if i == 0:
        json_data = json.loads(script.text)
        property_json['Details_Broad']['Number of Rooms'] = json_data['numberOfRooms'] 
        property_json['Details_Broad']['Floor Size (in sqft)'] = json_data['floorSize']['value'] 
        property_json['Address']['Street'] = json_data['address']['streetAddress'] 
        property_json['Address']['Locality'] = json_data['address']['addressLocality'] 
        property_json['Address']['Region'] = json_data['address']['addressRegion'] 
        property_json['Address']['Postal Code'] = json_data['address']['postalCode'] 
    if i == 1:
        json_data = json.loads(script.text)
        property_json['Price in $'] = json_data['offers']['price'] 
        property_json['Image'] = json_data['image'] 
    break


for div in soup.findAll('div', attrs={'id': 'ds-data-view'}):
    x = div.text.strip()
    print(x)



with open('data.json', 'w') as outfile:
    json.dump(property_json, outfile, indent=4)

with open('output_file.html', 'wb') as file:
    file.write(html)

print ('———-Extraction of data is complete. Check json file.———-')