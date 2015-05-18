import json
import string
import couchdb

USERNAME = 'team13'
PASSWORD = '1234qwer'

SERVER_URL = 'http://115.146.87.254:5984'
DB = 'suburb_boundaries' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
db = couch[DB]

cities = ['Ahwatukee Foothills', 'Alahambra', 'Camelback East',
'Central City', 'Deer Valley', 'Desert View', 'Encanto', 'Estrella',
'Laveen', 'Maryvale', 'North Gateway', 'North Mountain', 'Paradise Valley',
'New Village', 'South Mountain']

counter = 0
newArray = []
with open("PhoenixShape.json") as json_file:
    json_data = json.load(json_file)['features']
    for data in json_data:
        if 'NAME' in data['properties']:
            if data['properties']['NAME'] in cities:
                coord = data['geometry']['coordinates']
                newCoord = []
                for c in coord:
                    newCoord.append([c[1],c[0]])
                data['geometry']['coordinates'] = newCoord
                data['_id'] = data['properties']['NAME'].replace(' ', '_')
                try:
                    db.save(data)
                except Exception as e:
                    print (data["_id"], e)

#newArray.append(data['properties']['NAME'])
