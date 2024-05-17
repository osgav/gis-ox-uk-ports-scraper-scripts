#!/usr/bin/env python
#
# osgav
#
# web scraper for uk-ports.org
#
# 01: scrape links for individual ports from the port list page
#


import json
from bs4 import BeautifulSoup


## scraper-00 and scraper-01 use this
##
PORT_LIST_SOURCE_HTML = "./html/all-ports-list-page.html"

## scraper-01 and scraper-02 use this
##
PORT_LIST_URLS_JSON = "./json/all-ports-urls.json"


with open (PORT_LIST_SOURCE_HTML, "r") as file:
    az_listing = file.read()

soup = BeautifulSoup(az_listing, "lxml")

results = soup.find("div", class_="post-content")
more_results = results.find_all("a")

port_urls = {}

for result in more_results:
    if "ukports-a-to-z" in result.get('href'):
        port_name = result.get_text()
        port_url = result.get('href')
        port_urls[port_name] = port_url

with open (PORT_LIST_URLS_JSON, "w") as file:
    file.write(json.dumps(port_urls))
