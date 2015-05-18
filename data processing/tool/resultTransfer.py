import json
import couchdb

USERNAME = 'jollyjoker'
PASSWORD = '1234qwer'

SERVER_URL = 'http://115.146.93.135:5984'
DBMain = 'phoenix_tweets' ################################### change output
DBsuburb = 'suburb_boundaries'
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
dbMain = couch[DBcombined]
dbSuburb = couch[DBsuburb]

for doc in dbSuburb.view('_all_docs'):
    viewString = 'postcode/postcode_' + doc['id']
    myView = dbMain.view(viewString, reduce=False)
    tweetPOACount = str(myView.total_rows)
    print (doc['id'] + "," + tweetPOACount)
    data = dbSuburb[doc['id']]
    data['properties']['tweet_count'] = tweetPOACount
    dbSuburb.save(data)