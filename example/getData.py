import http.client
import time
from datetime import datetime

from mongoengine import connect, fields, Document

# Creating connection
mongo_database = connect(authentication_source='admin',
                         host='mongodb://3.120.160.125/test',
                         port=27017,
                         alias='main',
                         serverSelectionTimeoutMS=5000
                         )
headers = {"accept": "application/json", "x-cr-api-token": "e7f6e462a0e84cbab0dcae505cf54239",
           "Authorization": "Basic SEFYXENyZWF0aXZlTWVkdXNhOmVYeVQ5RiUzK0lvWXkmNw=="}
connection = http.client.HTTPSConnection('things.eu-1.bosch-iot-suite.com')


# The data model

class SmartThing(Document):
    thingId = fields.StringField(required=True)
    attributes = fields.DictField(required=True)
    energyConsumption = fields.FloatField(required=True)
    powerConsumption = fields.FloatField(required=True)
    lastSeen = fields.DateTimeField(required=True)
    switchState = fields.StringField(required=True)
    time = fields.DateTimeField(required=True)
    meta = {'db_alias': 'main'}


SMARTmacadresses = ["3A3014F711A0000495385ABCCE",
                    "3A3014F711A0000495385A11FB",
                    "3A3014F711A0000495385A110B"]


def getData(devicemac):
    import json
    connection.request("GET", "/api/2/things/com.bosch.bcx2019%3AHOME-hdm%3AHomeMaticIP%" + devicemac,
                       None,
                       headers)
    response = connection.getresponse()
    json = json.loads(response.read())

    # Assining Object
    mongo_object = {
        "thingId": json['thingId'],
        "attributes": json["attributes"],
        "energyConsumption": json['features']['powerMeter']['properties']['status']['value']['energyConsumption'],
        "powerConsumption": json['features']['powerMeter']['properties']['status']['value']['powerConsumption'],
        'switchState': json['features']['powerSwitch']['properties']['status']['value']['switchState'],
        'lastSeen': datetime.fromtimestamp(
            json['features']['connectivity']['properties']['status']['value']['lastSeen'] / 1e3),
        'time': datetime.now
    }

    print(mongo_object)
    if __name__ == '__main__':
        #   # Saving to MongoDB
        r = SmartThing(**mongo_object).save()
        # # Printing ID
    print(r.id)
    # pprint(datetime.datetime.fromtimestamp(1557831548493 / 1e3))


while True:
    getData(SMARTmacadresses[0])
    getData(SMARTmacadresses[1])
    getData(SMARTmacadresses[2])
    time.sleep(5)
