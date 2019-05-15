import csv
import json
import http.client
import time

# headers = {"accept": "application/json", "x-cr-api-token": "e7f6e462a0e84cbab0dcae505cf54239",
#          "Authorization": "Basic SEFYXENyZWF0aXZlTWVkdXNhOmVYeVQ5RiUzK0lvWXkmNw=="}

# connection = http.client.HTTPConnection('hackthonbxc2019.herokuapp.com')


import numpy

connection = http.client.HTTPConnection('localhost', 8000)


# The data model

def setAlert():
    connection.request("GET", "/status/alert")
    connection.close()


def getData():
    connection.request("GET", "/datasets/datasetGood")
    response = connection.getresponse()
    result = json.loads(response.read())
    with open('dataplug11fake.csv', 'r') as csvfile:
        for jsonobject in result:
            if jsonobject['attributes']['name'] == "Smart Plug 11":
                spamwriter = csv.writer(csvfile, delimiter=' ')
                if jsonobject['powerConsumption'] > 350:
                    spamwriter.writerow(
                        jsonobject['attributes']['name'] + "," + str(jsonobject['powerConsumption'] - 200))
                else:
                    spamwriter.writerow(jsonobject['attributes']['name'] + "," + str(jsonobject['powerConsumption']))


def checkSwitch():
    import json
    import datetime
    headers = {"accept": "application/json", "x-cr-api-token": "e7f6e462a0e84cbab0dcae505cf54239",
               "Authorization": "Basic SEFYXENyZWF0aXZlTWVkdXNhOmVYeVQ5RiUzK0lvWXkmNw=="}
    boschconnection = http.client.HTTPSConnection('things.eu-1.bosch-iot-suite.com')

    boschconnection.request("GET",
                            "/api/2/things/com.bosch.bcx2019%3AHOME-hdm%3AHomeMaticIP%3A3014F711A0001596D8599BEB",
                            None,
                            headers)
    response = boschconnection.getresponse()
    data = json.loads(response.read())
    timestamp1 = data['features']['keypad']['properties']['status']['value']['eventTimestamp']

    epoch = datetime.datetime.utcfromtimestamp(0)

    timestamp = (datetime.datetime.now() - epoch).total_seconds() * 1000.0

    if timestamp.__round__() - timestamp1 < 7205000:
        print("pressed")
        connection.request("GET", "/status/good")
        connection.close()
    else:
        print("not")


def analyseData():
    import pandas as pd
    d = pd.read_csv('dataplug11.csv')
    print(d.get_values())
    for row in d.get_values():
        print(float(row[0]))

    dfake = pd.read_csv('dataplug11fake.csv')
    dsfake = pd.read_csv('dataplug11SmallFake.csv')

    df = pd.DataFrame(d)

    # print(d['power'][0].dtypes)

    # analyseData()


setAlert()
while True:
    time.sleep(1)
    checkSwitch()
