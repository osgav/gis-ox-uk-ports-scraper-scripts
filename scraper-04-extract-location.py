#!/usr/bin/env python
#
# osgav 
#
# web scraper for uk-ports.org
#


import json
import os
from bs4 import BeautifulSoup

import re
import sys
import unicodedata


## scraper-02 and scraper-03 use this
##
PORT_PAGES_HTML_PATH = "./html/port-pages/"

PORT_LOCATIONS_RAW_JSON = "./json/all-ports-locations-raw-nocc.json"


# function for removing control chars from strings
# https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python/93029#93029
# https://stackoverflow.com/a/93029

all_chars = (chr(i) for i in range(sys.maxunicode))
categories = {'Cc'}
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) in categories)
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)




CLASS_PREFIX = "wpbdp-field-"

FIELDS_ALL = ["authority", "ownership", "contact", "transport_connections", "location", "storage", "uk_ports_association", "pilotage", "approximate_annual_tonnage", "port_contacts", "commercial_cargo_handling_facilities", "principal_activities", "access_and_accommodation", "facilities_and_services"]

#FIELDS_SUBSET = ["transport_connections", "location", "approximate_annual_tonnage", "principal_activities"]
#FIELDS_SUBSET = ["location", "approximate_annual_tonnage"]
FIELDS_SUBSET = ["location"]


port_pages = os.listdir(PORT_PAGES_HTML_PATH)
port_names = [port.removesuffix(".html") for port in sorted(port_pages)]

all_port_data = {}

for port in port_names:
    
    port_page_path = "{}{}{}".format(PORT_PAGES_HTML_PATH, port, ".html")
    
    with open(port_page_path, "r") as file:
        port_page_html = file.read()
    
    soup = BeautifulSoup(port_page_html, "lxml")
    
    port_details = soup.find("div", class_="listing-details")
    
    port_data = {}
    
    for field in FIELDS_SUBSET:
        class_name = "{}{}".format(CLASS_PREFIX, field)        
        try:
            port_field_all = port_details.find("div", class_=class_name)
            value = remove_control_chars(port_field_all.find("div", class_="value").text)
            #port_data[field] = port_field_all.find("div", class_="value").text
            port_data[field] = value
        except AttributeError:
            port_data[field] = "NO DATA: {}".format(field)
        except Exception as e:
            port_data[field] = "SCRIPT ERROR: {}".format(field)
            print("EXCEPTION PROCESSING {}: {}".format(port, field))
            print(e)
    
    all_port_data[port] = port_data


with open (PORT_LOCATIONS_RAW_JSON, "w") as file:
    file.write(json.dumps(all_port_data))
