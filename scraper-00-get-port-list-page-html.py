#!/usr/bin/env python
#
# osgav
#
# web scraper for uk-ports.org
#
# 00: download HTML source for port list
#


import requests


PORT_LIST_URL = "https://uk-ports.org/ukports-a-to-z-listing/"

## scraper-00 and scraper-01 use this
##
PORT_LIST_SOURCE_HTML = "./html/all-ports-list-page.html"

page = requests.get(PORT_LIST_URL)

with open(PORT_LIST_SOURCE_HTML, "w") as file:
    file.write(str(page.text))
