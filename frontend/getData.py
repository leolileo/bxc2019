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


class CarbonThing(Document):
    thingId = fields.StringField(required=True)
    attributes = fields.DictField(required=True)
    purity = fields.FloatField(required=True)
    temperature = fields.FloatField(required=True)
    humidity = fields.FloatField(required=True)
    lastSeen = fields.DateTimeField(required=True)
    time = fields.DateTimeField(required=True)
    meta = {'db_alias': 'main'}


SMARTmacadresses = ["3AHomeMaticIP%3A3014F711A0000495385ABCCE",
                    "3AHomeMaticIP%3A3014F711A0000495385A11FB",
                    "3AHomeMaticIP%3A3014F711A0000495385A110B"]

CO2macadresses = ["3AZigBee%3A000d6f000cb919c4"]


def getData(devicemac, carbon):
    import json
    connection.request("GET", "/api/2/things/com.bosch.bcx2019%3AHOME-hdm%" + devicemac,
                       None,
                       headers)
    response = connection.getresponse()
    json = json.loads(response.read())

    if carbon:
        mongo_object = {
            "thingId": json['thingId'],
            "attributes": json["attributes"],
            "purity": json['features']['airQuality']['properties']['status']['value']['purity'],
            "temperature": json['features']['airQuality']['properties']['status']['value']['temperature'],
            "humidity": json['features']['airQuality']['properties']['status']['value']['humidity'],
            'lastSeen': datetime.fromtimestamp(
                json['features']['connectivity']['properties']['status']['value']['lastSeen'] / 1e3),
            'time': datetime.now
        }
        r = CarbonThing(**mongo_object).save()
        # # Printing ID
        print(r.id)
    elif not carbon:
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
        r = SmartThing(**mongo_object).save()
        # # Printing ID
        print(r.id)


while True:
    for address in SMARTmacadresses:
        getData(address, False)
    for address in CO2macadresses:
        getData(address, True)
    time.sleep(5)
