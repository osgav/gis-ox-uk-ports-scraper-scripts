#!/usr/bin/env python
#
# osgav 
#
# web scraper for uk-ports.org
#


import json
import re

from lat_lon_parser import parse


PORT_LOCATIONS_RAW_JSON = "./json/all-ports-locations-raw-nocc-massaged.json"
PORT_TONNAGE_RAW_JSON = "./json/all-ports-tonnage-raw-massaged.json"


with open(PORT_LOCATIONS_RAW_JSON, "r") as file:
    port_locations_file = file.read()

port_locations = json.loads(port_locations_file)


with open(PORT_TONNAGE_RAW_JSON, "r") as file:
    port_tonnage_file = file.read()

port_tonnage = json.loads(port_tonnage_file)




def has_tonnage_data(port_name):
    try:
        int(port_tonnage[port_name]['approximate_annual_tonnage'])
        return True
    except ValueError as e:
        return False
    except Exception as e:
        print("EXCEPTION has_tonnage_data(): {}".format(e))
        return False




# function that takes text to be searched, and a list of regex patterns
# to search the text for

def test_patterns(text, patterns=[]):
	
	# empty list to be populated with match strings
	# and returned by the function
	matches = []

	# iterate through patterns passed in	
	for pattern in patterns:
		#print("Matching pattern: {}".format(pattern.pattern))
		# for each match found by the current pattern
		for match in re.findall(pattern, text):
			# add the match the the list 'matches'
			matches.append(match)
	return matches




#####################   REGEX FOR LAT-LON VARIATIONS

latlon_DMS_no_seconds = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo’′; NS] ?[NS]?;? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo’′; ] ?[EW])')

latlon_DMS_full = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo ’′] ?\d+[°⁰ºo ’′” NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo ’′] ?\d+[°⁰ºo ’′” EW]? ?[EW])')

latlon_DM_all_decimals = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+\.\d+[°⁰ºo’; NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+\.\d+[°⁰ºo’; EW]? ?[EW])', re.IGNORECASE)

latlon_DM_decimal_integer = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo’; NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+\.\d+[°⁰ºo’; EW]? ?[EW])')

latlon_DM_integer_decimal = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+\.\d+[°⁰ºo’; NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo’; EW]? ?[EW])')

latlon_DD = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+\.\d+[°⁰ºo’; NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+\.\d+[°⁰ºo’; EW]? ?[EW])')


for port_name, port_data in port_locations.items():
    location_raw = port_data['location']#
    
    matches = test_patterns(location_raw, [latlon_DMS_no_seconds, latlon_DMS_full, latlon_DM_all_decimals, latlon_DM_decimal_integer, latlon_DM_integer_decimal, latlon_DD,])

##### PRINT A CSV

#    if matches:
#        latlon = matches[0].split(";")
#        if len(latlon) == 2:
#            lat = parse(latlon[0])
#            lon = parse(latlon[1])
#            print("{},{},{}".format(port_name, lat, lon))

    if matches:
        latlon = matches[0].split(";")
        if len(latlon) == 2:
            lat = parse(latlon[0])
            lon = parse(latlon[1])
            ### NEW LOGIC for trying to grab tonnage data if there is a parsed location...
            if has_tonnage_data(port_name):
                tonnage = port_tonnage[port_name]['approximate_annual_tonnage']
                print("{},{},{},{}".format(port_name, lat, lon, tonnage))
