import csv
import http.client

# headers = {"accept": "application/json", "x-cr-api-token": "e7f6e462a0e84cbab0dcae505cf54239",
#          "Authorization": "Basic SEFYXENyZWF0aXZlTWVkdXNhOmVYeVQ5RiUzK0lvWXkmNw=="}

# connection = http.client.HTTPConnection('hackthonbxc2019.herokuapp.com')
import json

connection = http.client.HTTPConnection('localhost', 8000)


# The data model

def setAlert():
    connection.request("GET", "/status/alert")
    connection.close()


def getData():
    connection.request("GET", "/datasets/datasetGood")
    response = connection.getresponse()
    result = json.loads(response.read())
    with open('dataplug11fake.csv', 'w', newline='') as csvfile:
        for jsonobject in result:
            if jsonobject['attributes']['name'] == "Smart Plug 11":
                spamwriter = csv.writer(csvfile, delimiter=' ')
                if jsonobject['powerConsumption'] > 350:
                    spamwriter.writerow(
                        jsonobject['attributes']['name'] + "," + str(jsonobject['powerConsumption'] - 200))
                else:
                    spamwriter.writerow(jsonobject['attributes']['name'] + "," + str(jsonobject['powerConsumption']))


getData()
