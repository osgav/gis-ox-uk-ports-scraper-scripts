#!/usr/bin/env python
#
# osgav 
#
# web scraper for uk-ports.org
#


from bs4 import BeautifulSoup


## scraper-02 and scraper-03 use this
##
PORT_PAGES_HTML_PATH = "./html/port-pages/"

## TESTING
PORT_WICK = "./html/port-pages/warrenpoint.html"

with open(PORT_WICK, "r") as file:
    port_data_wick = file.read()

soup = BeautifulSoup(port_data_wick, "lxml")

port_details = soup.find("div", class_="listing-details")

# wpbdp-field-authority
# wpbdp-field-ownership
# wpbdp-field-contact
# wpbdp-field-transport_connections
# wpbdp-field-location
# wpbdp-field-storage
# wpbdp-field-uk_ports_association
# wpbdp-field-pilotage
# wpbdp-field-approximate_annual_tonnage
# wpbdp-field-port_contacts
# wpbdp-field-commercial_cargo_handling_facilities
# wpbdp-field-principal_activities
# wpbdp-field-access_and_accommodation
# wpbdp-field-facilities_and_services

field_prefix = "wpbdp-field-"

fields_all = ["authority", "ownership", "contact", "transport_connections", "location", "storage", "uk_ports_association", "pilotage", "approximate_annual_tonnage", "port_contacts", "commercial_cargo_handling_facilities", "principal_activities", "access_and_accommodation", "facilities_and_services"]

fields_subset = ["transport_connections", "location", "approximate_annual_tonnage", "principal_activities"]


#port_details_transport_connections = port_details.find("div", class_="wpbdp-field-transport_connections")
#print(port_details_transport_connections.prettify())
#print(port_details_transport_connections.text)
#value_port_details_transport_connections = port_details_transport_connections.find("div", class_="value")
#print(value_port_details_transport_connections.text)


port_data = {}

for field in fields_subset:
    class_name = "{}{}".format(field_prefix, field)
    port_data[field] = port_details.find("div", class_=class_name)


print(str(" ".join(port_data['location'].text.split())))

#for key, value in port_data.items():
#    print(value.text)
