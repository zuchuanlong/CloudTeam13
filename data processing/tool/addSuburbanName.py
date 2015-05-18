import couchdb
import urllib.request
import json

USERNAME = 'team13'
PASSWORD = '1234qwer'

SERVER_URL = 'http://115.146.87.254:5984'
DB = 'phoenix_tweets' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
db = couch[DB]
counter = 0
falseCounter = 0

cities = ['Ahwatukee Foothills', 'Alhambra', 'Camelback East',
'Central City', 'Deer Valley', 'Desert View', 'Encanto', 'Estrella',
'Laveen', 'Maryvale', 'North Gateway', 'North Mountain', 'Paradise Valley',
'New Village', 'South Mountain']

def isInTheList(name):
    for c in cities:
        if c.lower() in name.lower():
            return [True, c]
    return [False]

def getSuburbName(latString, lonString):
    global falseCounter
    try:
        geoGoogle = "http://maps.googleapis.com/maps/api/geocode/json?address="
        page = urllib.request.urlopen(geoGoogle+latString+','+lonString)
        pageString = page.read().decode("utf-8")
        json_data = json.loads(pageString)['results']
        for result in json_data:
            if 'neighborhood' in result['types']:
                for addr in result["address_components"]:
                    if 'neighborhood' in addr['types']:
                        tempResult = isInTheList(addr['long_name'])
                        if tempResult[0]:
                            return tempResult[1]
    except Exception as e:
        print (e)
    falseCounter += 1
    return "und"

for doc in db.view('suburban_marker/unmarked_even'):
    if (falseCounter >= 30):
        break
    if (counter >= 2500):
        break
    if (counter %100 == 0):
        print ("----",counter)
    data = db[str(doc['key'])]
    suburbName = getSuburbName(str(data['coordinates']['coordinates'][1]),str(data['coordinates']['coordinates'][0]))
    data['urban_village'] = suburbName
    print (suburbName)
    db.save(data)
    counter += 1
