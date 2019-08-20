import os
import csv
import re
import sys

consignees = []
consignees_full = []

name           = 0
addressLine    = 0
city           = 0
stateProvince  = 0
postalcode     = 0

description    = 0
quantity       = 0
packagingUnit  = 0
weight         = 0
weightUnit     = 0

def processed_yet(consignee):
    new = False
    for name in consignees:
        if name == consignee:
            new = True
    return new

def define_labels(line):
    
    labels = [
        "Consignee Name",
        "Consignee Address1",
        "Consignee City",
        "Consignee Province",
        "Consignee Postal Code",
        
        "Product Description",
        "Quantity",
        "Packaging Unit",
        "Net Weight",
        "Weight Unit"
        ]

    global name
    global addressLine
    global city
    global stateProvince
    global postalcode

    global description
    global quantity
    global packagingUnit
    global weight
    global weightUnit
    
    for part in line:
        for label in labels:
            if part == label:
                #print(part)
                #print(str(line.index(part)))
                if part == "Consignee Name":
                    name = line.index(part)
                if part == "Consignee Address1":
                    addressLine = line.index(part)
                if part == "Consignee City":
                    city = line.index(part)
                if part == "Consignee Province":
                    stateProvince = line.index(part)
                if part == "Consignee Postal Code":
                    postalcode = line.index(part)
                
                if part == "Product Description":
                    description = line.index(part)
                if part == "Quantity":
                    quantity = line.index(part)
                if part == "Packaging Unit":
                    packagingUnit = line.index(part)
                if part == "Net Weight":
                    weight = line.index(part)
                if part == "Weight Unit":
                    weightUnit = line.index(part) #Unused. Always "LBR"
    '''
    print("name at: " + str(name))
    print("addressLine at: " + str(addressLine))
    print("city at: " + str(city))
    print("province at: " + str(stateProvince))
    print("postal code at: " + str(postalcode))

    print("description at: " + str(description))
    print("quantity at: " + str(quantity))
    print("packaging unit at: " + str(packagingUnit))
    print("net weight at: " + str(weight))
    print("weight unit at: " + str(weightUnit))
    '''
         
#BEGIN

for arg in sys.argv[1:]:
    if not arg.endswith('.csv'): # Exit if a zip file wan't specified as an argument
        print('Error: Please use a .csv file')
        sys.exit()

out = open("out.json", "w+")
raw = list(csv.reader(open(arg)))

lines = []
for line in raw:
    templine = []
    for part in line:
        part = part.replace('"','')
        part = part.replace('\'','')
        templine.append(part)
    lines.append(templine)

define_labels(lines[1])
del lines[0]
del lines[0] #First two columns are labels

#ask for date
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
done = False
while done == False:
    date = input("Please enter the arrival date in the following format: YYYY-MM-DD\n")
    if date_pattern.match(date):
        done = True
        shipment = "726G" + date[0:4]+date[5:7]+date[8:10]
        print(shipment)
    else:
        print("Date entered in improper format")

#First part
out_text = ('{\n\t"data": "ACI_TRIP",\n\t"operation": "CREATE",\n\t"tripNumber": "' + shipment + '00",\n\t"portOfEntry": "0427",\n\t"estimatedArrivalDateTime": "' + date + ' 11:30:00",\n\t"estimatedArrivalTimeZone": "EST",\n\t"truck": {\n\t\t"number": "327618",\n\t\t"type": "BT",\n\t\t"vinNumber": "1FVACXCY3FHGN3106",\n\t\t"dotNumber": "3146045",\n\t\t"licensePlate": {\n\t\t\t"number": "7567PY",\n\t\t\t"stateProvince": "ON"\n\t\t}\n\t},\n\t"drivers": [\n\t\t{\n\t\t\t"firstName": "Jahan",\n\t\t\t"lastName": "Yazdanpanahi",\n\t\t\t"gender": "M",\n\t\t\t"dateOfBirth": "1958-09-17",\n\t\t\t"citizenshipCountry": "CA",\n\t\t\t"travelDocuments": [\n\t\t\t\t{\n\t\t\t\t\t"number": "Y09763830580917",\n\t\t\t\t\t"type": "5K",\n\t\t\t\t\t"stateProvince": "ON"\n\t\t\t\t},\n\t\t\t\t{\n\t\t\t\t\t"number": "HP553137",\n\t\t\t\t\t"type": "ACW",\n\t\t\t\t\t"country": "CA"\n\t\t\t\t}\n\t\t\t]\n\t\t}\n\t],\n\t"shipments": [\n')

#Find all the consignees
for line in lines:
    new = ''
    if not processed_yet(line[7]):
        consignees.append(line[7])
        consignees_full.append(line)

i = 1
for consignee in consignees:
    #print(consignee)
    index = consignees.index(consignee)
    #print("name: " + str(name) + ", index: " + str(index) + ", contents: " + consignees_full[index][name])
    out_text += ('\t\t{\n\t\t\t"data": "ACI_SHIPMENT",\n\t\t\t"operation": "CREATE",\n\t\t\t"shipmentType": "PARS",\n\t\t\t"loadedOn": {\n\t\t\t\t"type": "TRUCK",\n\t\t\t\t"number": "327618"\n\t\t\t},\n\t\t\t"cargoControlNumber": "' + shipment + str(i).zfill(2) + '",\n\t\t\t"referenceOnlyShipment": false,\n\t\t\t"portOfEntry": "0427",\n\t\t\t"releaseOffice": "0427",\n\t\t\t"estimatedArrivalDate": "' + date + ' 11:30:00",\n\t\t\t"estimatedArrivalTimeZone": "EST",\n\t\t\t"cityOfLoading": {\n\t\t\t\t"cityName": "Niagara Falls",\n\t\t\t\t"stateProvince": "NY"\n\t\t\t},\n\t\t\t"cityOfAcceptance": {\n\t\t\t\t"cityName": "Niagara Falls",\n\t\t\t\t"stateProvince": "NY"\n\t\t\t},\n\t\t\t"consolidatedFreight": false,\n\t\t\t"shipper": {\n\t\t\t\t"name": "Defranco Hardware",\n\t\t\t\t"address": {\n\t\t\t\t\t"addressLine": "3105 Pine Ave",\n\t\t\t\t\t"city": "Niagara Falls",\n\t\t\t\t\t"stateProvince": "NY",\n\t\t\t\t\t"postalCode": "14301"\n\t\t\t\t},\n\t\t\t\t"contactNumber": "716-285-3393"\n\t\t\t},\n\t\t\t"consignee": {\n\t\t\t\t"name": "' + consignees_full[index][name] + '",\n\t\t\t\t"address": {\n\t\t\t\t\t"addressLine": "' + consignees_full[index][addressLine] + '",\n\t\t\t\t\t"city": "' + consignees_full[index][city] + '",\n\t\t\t\t\t"stateProvince": "' + consignees_full[index][stateProvince] + '",\n\t\t\t\t\t"postalCode": "' + consignees_full[index][postalcode] + '"\n\t\t\t\t}\n\t\t\t},\n\t\t\t"commodities": [\n')
    for line in lines:
        if line[7] == consignee:
            #print(line[14])
            out_text += ('\t\t\t\t{\n\t\t\t\t\t"description": "' + line[description] + '",\n\t\t\t\t\t"quantity": ' + line[quantity] + ',\n\t\t\t\t\t"packagingUnit": "' + line[packagingUnit] + '",\n\t\t\t\t\t"weight": "' + line[weight] + '",\n\t\t\t\t\t"weightUnit": "LBR"\n\t\t\t\t},\n')
    out_text += ('\t\t\t],\n\t\t\t"autoSend": false\n\t\t},\n')
    i += 1
out_text += ('\t],\n\t"autoSend": false\n}')

#Remove a few troublesome comma
out_text = out_text.replace('},\n\t\t\t],','}\n\t\t\t],')
out_text = out_text.replace('},\n\t],\n\t"autoSend": false\n}','}\n\t],\n\t"autoSend": false\n}')
out_text = out_text.replace('\n",', '",')

print(out_text)
out.write(out_text)
out.close()
