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
    dataArray = []
    connection.request("GET", "/datasets/datasetGood")
    response = connection.getresponse()
    result = json.loads(response.read())
    for jsonobject in result:
        if jsonobject['attributes']['name'] == "Smart Plug 11":
            dataArray.append(jsonobject['powerConsumption'])
    return dataArray


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
    print(timestamp1)
    epoch = datetime.datetime.utcfromtimestamp(0)

    timestamp = (datetime.datetime.now() - epoch).total_seconds() * 1000.0

    if timestamp.__round__() - timestamp1 < 7205000:
        print("We got a signal!")
        connection.request("GET", "/status/good")
        connection.close()
        return True
    else:
        print("No signal yet!")
        return False


def analyseData():
    import pandas as pd
    dataArray = getData()
    frame = pd.DataFrame(dataArray)
    standarddev = frame.std()
    if standarddev[0] < 200:
        setAlert()
        while True:
            time.sleep(1)
            if checkSwitch():
                break


# analyseData()


while True:
    time.sleep(1)
    checkSwitch()
#    if checkSwitch():
#        break
