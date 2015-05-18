import sys
import re
import tweepy
import couchdb
import json
import jsonpickle
import string
import pickle
import time
from textblob import TextBlob
from nltk.corpus import wordnet as wn
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

#twitter access setup set 11 ################################### change output
CONSUMER_KEY = 'gUqrQCTseVfVDHYq4UxDhaB2t'
CONSUMER_SECRET = '12RLOFaTBWO05fBQldxTLLe9FyxXCphEuvWdP0uMEuFLqQYEOi'
ACCESS_TOKEN = '2781802950-UQorrMaAxLDsKuwpgJN6pKgGT9YQeMfIYExUlaa'
ACCESS_TOKEN_SECRET = 'fh9e86IUt2CDw3eoC2WcaB91OKuVHBzNU1BpAAMqzlJaD'
USERNAME = 'team13'
PASSWORD = '1234qwer'
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#couchdb access setup
SERVER_URL = 'http://115.146.87.254:5984'
DB = 'phoenix_tweets' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)

regexAt = re.compile(r"@(\w+)")

def expendKeywords(keywords):
    newKeywords = list(keywords)
    '''
    for keyword in keywords:
        try:
            syn = wn.synsets(keyword)[0]
            lemmas = syn.lemmas()
            for l in lemmas:
                newKeywords.append(l.name())
        except IndexError as e:
                continue
    '''
    st = LancasterStemmer()
    stemmed = [st.stem(word) for word in newKeywords]
    repeatRemoved = []
    for word in stemmed:
        if word not in repeatRemoved:
            repeatRemoved.append(word)
    return repeatRemoved

def getWords(docPath):
    raw = open(docPath,'r', encoding='utf-8')
    stemmed = []
    try:
        data = raw.read().replace('\n',' ').replace('_',' ')
        letters_only = re.sub("[^a-zA-Z0-9]", " ", data)
        lower_case = letters_only.lower()
        words = lower_case.split()
        words = [word for word in words if not word in stopwords.words("english")]
    except UnicodeDecodeError:
        print ("UnicodeDecodeError")
        pass
    #
    wordList = expendKeywords(words)
    return wordList

def containKeywords(text, keywords):
    letters_only = re.sub("[^a-zA-Z0-9]", " ", text)
    lower_case = letters_only.lower()
    words = lower_case.split()
    words = [word for word in words if not word in stopwords.words("english")]
    st = LancasterStemmer()
    stemmed = [st.stem(word) for word in words]
    return (any(i in stemmed for i in keywords))

def save_tweet(tweet):
    try:
        if tweet.id_str in db:
            pass
        else:
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
                
            if ((coordinates0 > -112.30) & (coordinates0 > 33.30) & (coordinates1 < -111.92) & (coordinates1 < 33.91)) | (placeFullName == 'Phoenix, AZ'):
                blob = TextBlob(doc['text'])
                doc['sentiment_score'] = blob.sentiment.polarity
                db[tweet.id_str] = (doc)
                #print (doc['user']['screen_name'])
                return regexAt.findall(doc['text'])
    except Exception as e:
        print (("---Encountered Exception:", e))
        pass
    return None

def userAllTweet(screenName):
    alltweets = []
    try:
        new_tweets = api.user_timeline(screen_name=screenName, count=200)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        
        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=screenName, count=200, max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
    except tweepy.TweepError:
        print ('We got a timeout ...')
        time.sleep(15*60)
        pass
    except IndexError:
        return alltweets
    except Exception as e:
        print ("---Encountered Exception userAllTweet: ", e)

    return alltweets

#pickle.dump([], open("/home/ubuntu/code/searched1.p","wb")) ################################### change output
#crimeKeywords = getWords('/home/ubuntu/twStream/crime.txt')

if __name__ == '__main__':
    try:
        db = couch.create(DB)
    except couchdb.http.PreconditionFailed as e:
        db = couch[DB]

    while (True):
        screenNames = pickle.load(open("/home/ubuntu/code/screenNames1.p", "rb")) ################################### change output
        searched1 = pickle.load(open("/home/ubuntu/code/searched1.p", "rb")) ################################### change output
        searched2 = pickle.load(open("/home/ubuntu/code/searched2.p", "rb")) ################################### change output
        searched3 = pickle.load(open("/home/ubuntu/code/searched3.p", "rb")) ################################### change output
        searched4 = pickle.load(open("/home/ubuntu/code/searched4.p", "rb")) ################################### change output
        allSearched = list(set(searched1)|set(searched2)|set(searched3)|set(searched4))
        secondarySearch = []
        if (len(screenNames)) > 0:
            screenName = screenNames[0]
            screenNames.remove(screenName)
            print ('search1 -- ', screenName, len(screenNames))
            pickle.dump(screenNames,open("/home/ubuntu/code/screenNames1.p","wb"))
            if screenName not in allSearched:
                tweets = userAllTweet(screenName)
                for t in tweets:
                    beingAted = save_tweet(t)
                    if beingAted != None:
                        secondarySearch += beingAted
                searched1.append(screenName)

        for second in secondarySearch:
            if second not in allSearched:
                tweets = userAllTweet(second)
                for t in tweets:
                    save_tweet(t)
            searched1.append(second)
        
        pickle.dump(searched1,open("/home/ubuntu/code/searched1.p","wb")) ################################### change output

