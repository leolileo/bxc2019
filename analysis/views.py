from django.http import HttpResponse
from mongoengine import Document, connect, fields

mongo_database = connect(authentication_source='admin',
                         host='mongodb://3.120.160.125/test',
                         port=27017,
                         alias='main',
                         serverSelectionTimeoutMS=5000
                         )


class SmartThing(Document):
    thingId = fields.StringField(required=True)
    attributes = fields.DictField(required=True)
    energyConsumption = fields.FloatField(required=True)
    powerConsumption = fields.FloatField(required=True)
    lastSeen = fields.DateTimeField(required=True)
    switchState = fields.StringField(required=True)
    time = fields.DateTimeField(required=True)
    meta = {'db_alias': 'main'}


limit = 1000


def good(request):
    a = SmartThing.objects().timeout(False).limit(limit)
    print(a.to_json())
    return HttpResponse(a.to_json(), content_type='application/json')


def problem(request):
    a = SmartThing.objects().timeout(False).limit(limit)
    print(a.to_json())
    return a.to_json()


def alert(request):
    a = SmartThing.objects().timeout(False).limit(limit)
    print(a.to_json())
    return a.to_json()
