import sys
import re
import tweepy
import couchdb
import json
import jsonpickle
import string
import pickle
from textblob import TextBlob
from nltk.corpus import wordnet as wn
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

#twitter access setup set 10 ################################### change output
CONSUMER_KEY = 'm9R4ciY6cmIWsWltTDJBVHdBv'
CONSUMER_SECRET = 'Hx3GiStd2GT2sQ2b419T0eelPAkqNo3m9NAAtopAiDizaCVjSG'
ACCESS_TOKEN = '2781675362-j91A25oPkeh414XMthgBLPBtHKUq5vrCmaE25X4'
ACCESS_TOKEN_SECRET = 'pDDxbW1dQbjx7QJKMlHzNjLQxL85UzAipsilaYsb6E2ZP'
USERNAME = 'team13'
PASSWORD = '1234qwer'
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#couchdb access setup
SERVER_URL = 'http://115.146.87.254:5984'
DB = 'phoenix_tweets' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
screenNames = []
#pickle.dump(screenNames, open( "screenNames1.p", "wb" ))################################### change output
location = [-112.30, 33.30, -111.92, 33.61]
outputSwitcher = 0

def print_tweet(tweet):
    pickled = jsonpickle.encode(tweet)
    results = json.loads(pickled)
    doc = results['py/state']['_json']
    print ("@%s - %s (%s)" % (doc['user']['screen_name'], doc['user']['name'], doc['created_at']))
    print (doc['text'])
    
def save_tweet(tweet):
    try:
        if tweet.id_str in db:
            pass
        else :
            pickled = jsonpickle.encode(tweet)
            results = json.loads(pickled)
            doc = results['py/state']['_json']
            if (doc['coordinates'] != None):
                coordinates0 = doc['coordinates']['coordinates'][0]
                coordinates1 = doc['coordinates']['coordinates'][1]
            else:
                coordinates0 = 0
                coordinates1 = 0
            if doc['place'] != None:
                placeFullName = doc['place']['full_name']
            else:
                placeFullName = None
                
            if ((coordinates0 > -112.30) & (coordinates0 > 33.30) & (coordinates1 < -111.92) & (coordinates1 < 33.91)) | (doc['place']['full_name'] == 'Phoenix, AZ'):
                blob = TextBlob(doc['text'])
                doc['sentiment_score'] = blob.sentiment.polarity
                db[tweet.id_str] = (doc)
                return doc['user']['screen_name']
    except Exception as e:
        print (("---Exception in save_tweet:", e))
        pass
    return None

def userAllTweet(screenName):
    alltweets = []  
    new_tweets = api.user_timeline(screen_name=screenName, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screenName, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
    return alltweets

def nameOutput(screenName, outputSwitcher):
    if outputSwitcher%4 == 0:
        screenNames = pickle.load(open("/home/ubuntu/code/screenNames1.p","rb")) ################################### change output
        if screenName not in screenNames:
            if screenName != None:
                outputSwitcher += 1
                outputSwitcher = outputSwitcher%4
                screenNames.append(screenName)
        pickle.dump(screenNames, open("/home/ubuntu/code/screenNames1.p","wb")) ################################### change output
    elif outputSwitcher%4 == 1:
        screenNames = pickle.load(open("/home/ubuntu/code/screenNames2.p","rb")) ################################### change output
        if screenName not in screenNames:
            if screenName != None:
                outputSwitcher += 1
                outputSwitcher = outputSwitcher%4
                screenNames.append(screenName)
        pickle.dump(screenNames, open("/home/ubuntu/code/screenNames2.p","wb")) ################################### change output
    elif outputSwitcher%4 == 2:
        screenNames = pickle.load(open("/home/ubuntu/code/screenNames3.p","rb")) ################################### change output
        if screenName not in screenNames:
            if screenName != None:
                outputSwitcher += 1
                outputSwitcher = outputSwitcher%4
                screenNames.append(screenName)
        pickle.dump(screenNames, open("/home/ubuntu/code/screenNames3.p","wb")) ################################### change output
    else:
        screenNames = pickle.load(open("/home/ubuntu/code/screenNames4.p","rb")) ################################### change output
        if screenName not in screenNames:
            if screenName != None:
                outputSwitcher += 1
                outputSwitcher = outputSwitcher%4
                screenNames.append(screenName)
        pickle.dump(screenNames, open("/home/ubuntu/code/screenNames4.p","wb")) ################################### change output
    return outputSwitcher

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    #crimeKeywords = getWords('/home/ubuntu/twStream/crime.txt')
    global outputSwitcher

    def on_status(self, data):
        screenName = save_tweet(data)
        if screenName != None:
            try:
                self.outputSwitcher = nameOutput(screenName, self.outputSwitcher)
            except Exception as e:
                print (e)
        return True

    def on_error(self, status):
        print ("error%s" % status)

        return True

    def on_timeout(self):
        return True

if __name__ == '__main__':
    try:
        db = couch.create(DB)
    except couchdb.http.PreconditionFailed as e:
        db = couch[DB]

    l = StdOutListener()

    print ("Steaming starts!")

    #tweets = userAllTweet('DreamloveInt')

    stream = tweepy.Stream(auth, l)
    stream.filter(locations=location) ################################### change output