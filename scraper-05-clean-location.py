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


with open(PORT_LOCATIONS_RAW_JSON, "r") as file:
    port_locations_file = file.read()

port_locations = json.loads(port_locations_file)


latlon_01 = re.compile(r'^Lat: \d+[º] \d+[’] [NS]; Long: \d+[º] \d+[’] [EW]') 
# latlon_01 based on aberaeron, 6 matches

latlon_02 = re.compile(r'^\d+.\d+[°] [NS], \d+.\d+[°] [EW]')
# latlon_02 based on aberdeen, 1 match

latlon_03 = re.compile(r'^Lat: \d+[⁰] \d+[⁰] [NS] Long: \d+[⁰] \d+[⁰][EW]')
# latlon_03 based on aberdour-harbour, 1 match

latlon_04 = re.compile(r'^Lat: \d+[⁰] \d+[⁰] \d[NS] Long: \d+[⁰] \d+[⁰] \d+[NSEW]')
# latlon_04 based on aberdyfi, 1 match

latlon_05 = re.compile(r'^Lat: \d+[º] \d+[′] [NS]; Long: \d+[º] \d+[′] [EW]')
# latlon_05 based on aberystwyth, 1 match

latlon_06 = re.compile(r'^\d+[º] \d+[′].\d+ [NS] \d+[º] \d+[′].\d+[EW]')
# latlon_06 based on amlwch-port, 1 match

latlon_07 = re.compile(r'^Lat: \d+[º] \d+[′] N Long: \d+[º] \d+[′] [EW]')
# latlon_07 based on anstruther, 1 match

latlon_08 = re.compile(r'^Lat: \d+[⁰] \d+[⁰] [NS]; Long: \d+[⁰] \d+[⁰] [EW]')
# latlon_08 based on arbroath, 1 match

latlon_09 = re.compile(r'^Lat: \d+[⁰] \d+[⁰][NS]; Long: \d+[⁰] \d+[⁰] [EW]')
# latlon_09 based on ardglass, 1 match

latlon_10 = re.compile(r'^Lat: \d+[⁰] \d+.\d+[⁰] [NS]; Long: \d+[⁰] \d+.\d+[⁰] [EW]')
# latlon_10 based on ardrishhaig, 1 match

latlon_11 = re.compile(r'^Lat: \d+[°] \d+[’] [NS]; Long \d+[°] \d+[’] [EW]')
# latlon_11 based on ardrosson, 2 matches !!!

latlon_12 = re.compile(r'^Lat: \d+[°] \d+[’] [NS]; Long: \d+[°] \d+[’] [EW]')
# latlon_12 based on ayr, 28 matches wahey !!!


#####################   REGEX FOR LAT-LON VARIATIONS


latlon_DMS_no_seconds = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo’′; NS] ?[NS]?;? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo’′; ] ?[EW])')

latlon_DMS_full = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo ’′] ?\d+[°⁰ºo ’′” NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo ’′] ?\d+[°⁰ºo ’′” EW]? ?[EW])')

latlon_DM_all_decimals = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+\.\d+[°⁰ºo’; NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+\.\d+[°⁰ºo’; EW]? ?[EW])', re.IGNORECASE)

latlon_DM_decimal_integer = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo’; NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+\.\d+[°⁰ºo’; EW]? ?[EW])')

latlon_DM_integer_decimal = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+[°⁰ºo ] ?\d+\.\d+[°⁰ºo’; NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+[°⁰ºo ] ?\d+[°⁰ºo’; EW]? ?[EW])')

latlon_DD = re.compile(r'^((?:Latitude|Lat)?[:.]? ?\d+\.\d+[°⁰ºo’; NS]? ?[NS]?[;,]? (?:Longitude|Long)?[:.]? ?\d+\.\d+[°⁰ºo’; EW]? ?[EW])')


for port_name, port_data in port_locations.items():
    location_raw = port_data['location']
    
    #location_list = location_raw.split()
    #print(location_list)
#    print(location_raw)
    
#    matches = test_patterns(location_raw, [latlon_01,])
#    matches = test_patterns(location_raw, [latlon_12,])

#    matches = test_patterns(location_raw, [latlon_DMS_no_seconds,])
#    matches = test_patterns(location_raw, [latlon_DMS_full,])
#    matches = test_patterns(location_raw, [latlon_DM_all_decimals,])
#    matches = test_patterns(location_raw, [latlon_DM_decimal_integer,])
#    matches = test_patterns(location_raw, [latlon_DM_integer_decimal,])
#    matches = test_patterns(location_raw, [latlon_DD,])

    matches = test_patterns(location_raw, [latlon_DMS_no_seconds, latlon_DMS_full, latlon_DM_all_decimals, latlon_DM_decimal_integer, latlon_DM_integer_decimal, latlon_DD,])    

    ##print(matches)
#    print(len(matches))

#    print("{}: {}".format(len(matches), port_name))

#    if not matches:
#        print("{}|  {}".format(port_name, location_raw))
#        print(" ".join(location_raw.split()))
#        print(location_raw.split())
#        print(location_raw)


##### PRINT A CSV

    if matches:
        latlon = matches[0].split(";")
        if len(latlon) == 2:
            lat = parse(latlon[0])
            lon = parse(latlon[1])
            print("{},{},{}".format(port_name, lat, lon))
