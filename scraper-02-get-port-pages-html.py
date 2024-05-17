#!/usr/bin/env python
#
# osgav
#
# web scraper for uk-ports.org
#
# 02: download HTML source for all the individual port pages
#


import json
import requests
import time


## scraper-01 and scraper-02 use this
##
PORT_LIST_URLS_JSON = "./json/all-ports-urls.json"

## scraper-02 and scraper-03 use this
##
PORT_PAGES_HTML_PATH = "./html/port-pages/"


def save_page(name, content):
    filename = "{}{}.html".format(PORT_PAGES_HTML_PATH, name)
    with open(filename, "w") as file:
        file.write(str(content.text))

def download_page(url):
    return requests.get(url)


with open (PORT_LIST_URLS_JSON, "r") as file:
    ports_json = file.read()

port_urls = json.loads(ports_json)

#for url in list(port_urls.values())[-6:-2]:
for url in list(port_urls.values()): ### FULL PORT LIST
    port_name = url.split("/")[-2]
    print("[+] downloading page: {}".format(port_name))
    page = download_page(url)
    save_page(port_name, page)
    time.sleep(1)
