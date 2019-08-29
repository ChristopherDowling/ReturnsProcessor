import os
import csv
import re
import sys

consignees = []
consignees_full = []

name           = 0
addressline    = 0
city           = 0
stateProvince  = 0
postalcode     = 0
idNumber       = 0

description    = 0
quantity       = 0
packagingUnit  = 0
weight         = 0
weightUnit     = 0
marksAndNumbers = 0

def processed_yet(consignee):
    new = False
    for name in consignees:
        if name == consignee:
            new = True
    return new

#Finds the index for each label eg. "Consignee Name" at index 7
def define_labels(line):
    labels = [
        "Consignee Name",
        "Consignee Address1",
        "Consignee City",
        "Consignee Province",
        "Consignee Postal Code",
        "Congsinee ID No.",
        
        "Product Description",
        "Quantity",
        "Packaging Unit",
        "Net Weight",
        "Weight Unit",
        "Shipment ID"
        ]

    global marksAndNumbers
    global name
    global addressline
    global city
    global stateProvince
    global postalcode
    global idNumber

    global description
    global quantity
    global packagingUnit
    global weight
    global weightUnit
    
    for part in line:
        for label in labels:
            if part == label:
                if part == "Consignee Name":
                    name = line.index(part)
                if part == "Consignee Address1":
                    addressline = line.index(part)
                if part == "Consignee City":
                    city = line.index(part)
                if part == "Consignee Province":
                    stateProvince = line.index(part)
                if part == "Consignee Postal Code":
                    postalcode = line.index(part)
                if part == "Congsinee ID No.":
                    idNumber = line.index(part)
                
                if part == "Product Description":
                    description = line.index(part)
                if part == "Quantity":
                    quantity = line.index(part)
                if part == "Packaging Unit":
                    packagingUnit = line.index(part) # Unused?
                if part == "Net Weight":
                    weight = line.index(part)
                if part == "Weight Unit":
                    weightUnit = line.index(part) #Unused. Always "LBR"
                if part == "Shipment ID":
                    marksAndNumbers = line.index(part)
         
#BEGIN

for arg in sys.argv[1:]:
    if not arg.endswith('.csv'): # Exit if a zip file wan't specified as an argument
        print('Error: Please use a .csv file')
        sys.exit()

out = open("out.json", "w+")
error = open("errors.txt", "w+")
error_text = ''
raw = list(csv.reader(open(arg)))
slips_folder = os.getcwd() + "\\slips\\"
if not os.path.exists(slips_folder):
    os.mkdir(slips_folder)

define_labels(raw[1])

#Clears out quotation marks and other unacceptable characters
lines = []
i = 0
for line in raw:
    i += 1
    templine = []
    for part in line:
        part = part.replace('"','')
        part = part.replace('\'','')
        templine.append(part)
    if not templine[name] == '' and not templine[addressline]== '' and not templine[city] == '' and not templine[stateProvince]== '' and not templine[postalcode] == '' and not templine[description]== '' and not templine[quantity] == '' and not templine[packagingUnit]== '' and not templine[weight] == '' and not templine[weightUnit] == '':
        lines.append(templine)
        #print(str(i), templine[name])
    elif templine[name] == '' and templine[addressline]== '' and templine[city] == '' and templine[stateProvince]== '' and templine[postalcode] == '' and templine[description]== '' and templine[quantity] == '' and templine[packagingUnit]== '' and templine[weight] == '' and templine[weightUnit] == '':
        #print(str(i), "[ERROR: EMPTY line]")
        z = 0 # Empty line
    else:
        #print(str(i), "[ERROR: MISSING DATA]")
        error_text = error_text + str(i) + " [ERROR: MISSING DATA]\n"

del lines[0] #First two columns are labels

#ask for date
date_pattern = re.compile(r'\d{2}-\d{2}-\d{2}')
done = False
while done == False:
    date = input("Please enter the arrival date in the following format: YY-MM-DD\n")
    if date_pattern.match(date):
        done = True
        shipment = "726G" + date[0:2]+date[3:5]+date[6:8] + "RT"
        #print(shipment)
    else:
        print("Date entered in improper format")

# First, kinda static part of the .json
out_text = ('{\n\t"data": "ACI_TRIP",\n\t"operation": "CREATE",\n\t"tripNumber": "' + shipment + '00",\n\t"portOfEntry": "0427",\n\t"estimatedArrivalDateTime": "' + date + ' 11:30:00",\n\t"estimatedArrivalTimeZone": "EST",\n\t"truck": {\n\t\t"number": "327618",\n\t\t"type": "BT",\n\t\t"vinNumber": "1FVACXCY3FHGN3106",\n\t\t"dotNumber": "3146045",\n\t\t"licensePlate": {\n\t\t\t"number": "7567PY",\n\t\t\t"stateProvince": "ON"\n\t\t}\n\t},\n\t"drivers": [\n\t\t{\n\t\t\t"firstName": "Jahan",\n\t\t\t"lastName": "Yazdanpanahi",\n\t\t\t"gender": "M",\n\t\t\t"dateOfBirth": "1958-09-17",\n\t\t\t"citizenshipCountry": "CA",\n\t\t\t"travelDocuments": [\n\t\t\t\t{\n\t\t\t\t\t"number": "Y09763830580917",\n\t\t\t\t\t"type": "5K",\n\t\t\t\t\t"stateProvince": "ON"\n\t\t\t\t},\n\t\t\t\t{\n\t\t\t\t\t"number": "HP553137",\n\t\t\t\t\t"type": "ACW",\n\t\t\t\t\t"country": "CA"\n\t\t\t\t}\n\t\t\t]\n\t\t}\n\t],\n\t"shipments": [\n')

#Find all the consignees
for line in lines:
    new = ''
    if not processed_yet(line[name]):
        consignees.append(line[name])
        consignees_full.append(line)

#For each Consignee, and for each shipment per consignee, print the .json stuff
i = 0
for consignee in consignees:
    index = consignees.index(consignee)
    # Per consignee, add shipment details
    out_text += ('\t\t{\n\t\t\t"data": "ACI_SHIPMENT",\n\t\t\t"operation": "CREATE",\n\t\t\t"shipmentType": "PARS",\n\t\t\t"loadendOn": {\n\t\t\t\t"type": "TRUCK",\n\t\t\t\t"number": "327618"\n\t\t\t},\n\t\t\t"cargoControlNumber": "' + shipment + str(i+1).zfill(2) + '",\n\t\t\t"referenceOnlyShipment": false,\n\t\t\t"portOfEntry": "0427",\n\t\t\t"releaseOffice": "0427",\n\t\t\t"estimatedArrivalDate": "20' + date + ' 11:30:00",\n\t\t\t"estimatedArrivalTimeZone": "EST",\n\t\t\t"cityOfLoading": {\n\t\t\t\t"cityName": "Niagara Falls",\n\t\t\t\t"stateProvince": "NY"\n\t\t\t},\n\t\t\t"cityOfAcceptance": {\n\t\t\t\t"cityName": "Niagara Falls",\n\t\t\t\t"stateProvince": "NY"\n\t\t\t},\n\t\t\t"consolidatedFreight": false,\n\t\t\t"shipper": {\n\t\t\t\t"name": "Defranco Hardware",\n\t\t\t\t"address": {\n\t\t\t\t\t"addressline": "3105 Pine Ave",\n\t\t\t\t\t"city": "Niagara Falls",\n\t\t\t\t\t"stateProvince": "NY",\n\t\t\t\t\t"postalCode": "14301"\n\t\t\t\t},\n\t\t\t\t"contactNumber": "716-285-3393"\n\t\t\t},\n\t\t\t"consignee": {\n\t\t\t\t"name": "' + consignees_full[index][name] + '",\n\t\t\t\t"address": {\n\t\t\t\t\t"addressline": "' + consignees_full[index][addressline] + '",\n\t\t\t\t\t"city": "' + consignees_full[index][city] + '",\n\t\t\t\t\t"stateProvince": "' + consignees_full[index][stateProvince] + '",\n\t\t\t\t\t"postalCode": "' + consignees_full[index][postalcode] + '"\n\t\t\t\t}\n\t\t\t},\n\t\t\t"commodities": [\n')
    # Per consignee, creater a packign slip for them
    slip = open(slips_folder + consignee.replace('/', '') + ".rtf", "w+")
    slip_text = '{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat\\deflang1033\\deflangfe1033{\\fonttbl{\\f0\\fnil\\fcharset0 Lucida Console;}}\\n{\\*\\generator Riched20 10.0.10586}{\\*\\mmathPr\\mdispDef1\\mwrapIndent1440 }\\viewkind4\\uc1 \\n\\pard\\nowidctlpar\\sa200\\sl276\\slmult1\\qr\\b\\f0\\fs40\\lang9 PACKING SLIP\\b0\\fs22\\par\\n 20' + str(date) + '\\par CID: ' + consignees_full[index][idNumber] + '\\b0\\fs22\\par\\n\\pard\\nowidctlpar\\sa200\\sl276\\slmult1 DeFranco Hardware\\line 3105 Pine Ave, Niagara Falls, NY, 14301\\line 1-877-863-7447\\par\\n SHIP TO:\\line ' + str(consignee) + '\\line ' + consignees_full[index][addressline] +' '+ consignees_full[index][addressline+1] + '\\line ' + consignees_full[index][addressline+2] + ', ' + consignees_full[index][addressline+3] + '\\line Canada\\par\\n ORDER DATE\\tab\\tab PURCHASE ORDER\\line 20' + str(date) + '\\tab\\tab ' + str(shipment) + str(index+1).zfill(2) + '\\par\\n ORDER Q#\\tab SHIP Q#\\tab ITEM\\line '
    
    total = 0
    total2 = 0
    for line in lines:
        if line[name] == consignee:
            # Per commodity, add it to the consignee's shitpment
            out_text += ('\t\t\t\t{\n\t\t\t\t\t"description": "' + line[description] + '",\n\t\t\t\t\t"quantity": ' + line[quantity] + ',\n\t\t\t\t\t"packagingUnit": "' + line[packagingUnit] + '",\n\t\t\t\t\t"weight": "' + line[weight] + '",\n\t\t\t\t\t"weightUnit": "LBR",\n\t\t\t\t\t"marksAndNumbers": "' + line[marksAndNumbers] + '"\n\t\t\t\t},\n')
            slip_text += line[quantity] + '\\tab\\tab 1\\tab\\tab ' + line[description] + '\\line '
            total += int(line[quantity])
            total2 += 1
    # Finish off the consignee
    out_text += ('\t\t\t],\n\t\t\t"autoSend": false\n\t\t},\n')
    # Finish the loading slip
    slip_text += '---------------------------\\line ' + str(total) + '\\tab\\tab ' + str(total2) + '\\tab\\tab TOTAL\\par\\n}' 
    slip.write(slip_text)
    slip.close()
    
    i += 1
out_text += ('\t],\n\t"autoSend": false\n}')

#Remove a few troublesome comma
out_text = out_text.replace('},\n\t\t\t],','}\n\t\t\t],')
out_text = out_text.replace('},\n\t],\n\t"autoSend": false\n}','}\n\t],\n\t"autoSend": false\n}')
out_text = out_text.replace('\n",', '",')

#print(out_text)
out.write(out_text)
out.close()
error.write(error_text)
error.close()

input("Press Enter to exit")
