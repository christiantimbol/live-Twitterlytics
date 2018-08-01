'''
###############################################################
###############################################################
twitter.py

problems with messy_twitter.py:
  - global variables!! they're hard to track and maintain
  - functions are spread throughout the code and having classes would allow easier management/testing
  - does not pass stats to main function which makes storing and manipulating stats data problematic
  - does not pass data from Streaming API to main function. since the streaming data is real time, processing (writing to DB) should not be done in the streaming. the solution to this is to create a class to store statistics which will store the data as Python objects and minimize the read/write time

after organizing the code from messy_twitter.py to what is seen here in twitter.py:
  - this code passes data collected in twitter_listener() class to MainTwitter() class without global variables
  - the method is quicker since objects are being stored in memory
  - reading/writing stats in multiple places is now possible, which allows one function to update them and another to be reading them

check messy_twitter.py to see the corresponding changes from that file and this file :-)

IMPORTANT:

before beginning, ensure to input the following into the terminal after activating a virtual environment to install the necessary packages...

> pip install -r reqs.txt
###############################################################
###############################################################
'''

# Tweepy API
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
# Python Debugger
import pdb
import json
from collections import Counter
# Database
import sqlite3
# Twitter App Authentication
from credentials import *
# Regular Expressions
import re
import time

db = "twitterlytics_data.db"

countries_list = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina', 'Burundi', 'Cameroon', 'Cape Verde', 'Central African Republic', 'Chad', 'Comoros', 'Congo', '"Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Swaziland', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe', 'Afghanistan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Burma (Myanmar)', 'Cambodia', 'China', 'East Timor', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', '"Korea', '"Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Nepal', 'Oman', 'Pakistan', 'Philippines', 'Qatar', 'Russian Federation', 'Saudi Arabia', 'Singapore', 'Sri Lanka', 'Syria', 'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen', 'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City', 'Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States', 'Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu', 'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']

# Twitter's JSON object returns languages as a 2-character code under the lang json key, so this 'langs' python dictionary will convert the 2-char code to the corresponding language name
langs = \
    {'ar': 'Arabic',
     'bg': 'Bulgarian',
     'ca': 'Catalan',
     'cs': 'Czech',
     'da': 'Danish',
     'de': 'German',
     'el': 'Greek',
     'en': 'English',
     'es': 'Spanish',
     'et': 'Estonian',
     'fa': 'Persian',
     'fi': 'Finnish',
     'fr': 'French',
     'hi': 'Hindi',
     'hr': 'Croatian',
     'hu': 'Hungarian',
     'id': 'Indonesian',
     'is': 'Icelandic',
     'it': 'Italian',
     'iw': 'Hebrew',
     'ja': 'Japanese',
     'ko': 'Korean',
     'lt': 'Lithuanian',
     'lv': 'Latvian',
     'ms': 'Malay',
     'nl': 'Dutch',
     'no': 'Norwegian',
     'pl': 'Polish',
     'pt': 'Portuguese',
     'ro': 'Romanian',
     'ru': 'Russian',
     'sk': 'Slovak',
     'sl': 'Slovenian',
     'sr': 'Serbian',
     'sv': 'Swedish',
     'th': 'Thai',
     'tl': 'Filipino',
     'tr': 'Turkish',
     'uk': 'Ukrainian',
     'ur': 'Urdu',
     'vi': 'Vietnamese',
     'zh_CN': 'Chinese (simplified)',
     'zh_TW': 'Chinese (traditional)'
     }

swear_words = ["fuck", "shit", "bitch", "idiot"]

love_words = ["love", "thank", "happy", "bless"]


class Twit_utils():

  def __init__(self, api):
    self.api = api

  def get_tweet_html(self, id):
    oembed = self.api.get_oembed(id=id, hide_media=True, hide_thread=True)

    tweet_html = oembed['html'].strip("\n")

    return tweet_html

# creating stats() class to store the data in Python dictionaries after the dictionary converts the 2-char lang into the corresponding language. since the data is stored as Python objects in memory, it can be used in different places. it's created once and passes the object around. this is a solution to global variables because if the code needs to be changed, it only needs to be done once.


class stats():

  def __init__(self):
    self.lang = []
    self.top_lang = []
    self.love_words = 0
    self.swear_words = 0
    self.top_tweets = []
    self.countries = []
    self.tweets_grabbed = 0

  def add_lang(self, lang):
    self.lang.append(lang)

  def add_top_lang(self, top_lang):
    self.top_lang.append(top_lang)

  def love_word_found(self):
    self.love_words += 1

  def swear_word_found(self):
    self.swear_words += 1

  def save_top_tweets(self, tweet_html):
    self.top_tweets.append(tweet_html)

  def add_country(self, country):
    self.countries.append(country)

  def set_tweets_grabbed(self):
    self.tweets_grabbed += 1

  def get_tweets_grabbed(self):
    return self.tweets_grabbed

  def get_stats(self):
    return self.lang, self.top_lang, self.love_words, self.swear_words, self.top_tweets, self.countries

# creating twitter_listener() class which gets streaming data. twitter_listener() class is inherited from Tweepy's StreamListener.


class listener(StreamListener):

  '''
  - adding a counter to make code stop since code keeps running until killed in terminal with Ctrl+C. counter can not be added to on_data() because on_data() is newly called every time. so, counter is added to twitter_listener class during initialization function __init__() so the counter will be available each time on_data() is called

  - __init__() function called when twitter_listener class created. passing in number_tweets_to_grab variable. internal counter is initialized in main code

  - top tweets defined as tweets that exceed 10,000 retweets. added retweet_count parameter to __init__() function, initialized by quantification of what constitutes a top tweet. this quantification may be changed according to subjective definition of top tweet
  '''

  def __init__(self, stats_obj, twit_utils, num_tweets_to_grab, retweet_count):
    self.count = 0
    # stats object passed to twitter_listener class
    self.stats_obj = stats_obj
    self.twit_utils = twit_utils
    # num_tweets_to_grab: The number of tweets to grab. If this number is too big, Twitter blocks you temporarily, so keep it small.
    self.num_tweets_to_grab = num_tweets_to_grab
    # retweet_count: The number of times a tweet must have been retweeted for us to save it.
    self.retweet_count = retweet_count
    self.tweets_grabbed = 0

  # on_data() function tells Tweepy what to do when new Tweet is available. in this case, on_data() loads json data using the inbuilt json library and prints the text of the tweets
  def on_data(self, data):
    try:
      json_data = json.loads(data)
      # uncomment for test to check if json_data is received
      # print(json_data)

      tweet = json_data["text"]

      for l in love_words:
        if l in tweet.lower():
          self.stats_obj.love_word_found()

      for l in swear_words:
        if l in tweet.lower():
          self.stats_obj.swear_word_found()

      for country in countries_list:
        country_local = "\\b" + country + "\\b"
        if re.findall(country_local, tweet, flags=re.IGNORECASE):
          self.stats_obj.add_country(country)

      # Hack for USA & UK, since no one uses its full name on Twitter
      # Yes, it's unfair I'm not doing this for all countries.
      if re.findall("\\busa\\b", tweet, flags=re.IGNORECASE):
        self.stats_obj.add_country("United States")

      if re.findall("\\bbritain\\b", tweet, flags=re.IGNORECASE):
        self.stats_obj.add_country("United Kingdom")

      # get retweet_count by parsing twitter json object
      retweet_count = json_data["retweeted_status"]["retweet_count"]

      # stores language in lang list in stats() class
      self.stats_obj.add_lang(langs[json_data["lang"]])

      # checks if tweet's retweet_count is > retweet_count for self-defined top tweet (>10000). if passes, prints tweet text, tweet retweet_count, tweet lang, then saves language
      # ToDo '@2' see if I can add code to retweet the tweet if it's a top tweet
      if retweet_count > self.retweet_count:
        print (tweet, retweet_count, langs[json_data["lang"]])
        self.stats_obj.add_top_lang(langs[json_data["lang"]])
        tweet_html = self.twit_utils.get_tweet_html(json_data['id'])
        self.stats_obj.save_top_tweets(tweet_html)

      self.count += 1
      self.stats_obj.set_tweets_grabbed()

      if self.count == self.num_tweets_to_grab:
        # returning false causes class to exit after reaching the specified number_tweets_to_grab (which is how Tweepy internally works).
        return False

      return True

    except:
      # @1 !!!ToDo: this is bad/dangerous because instead of fixing problem, problems are just hidden. bad tweets along with bugs in the code will just be hidden.
      # pdb.set_trace()
      pass

  '''
  on_error() function prints error status if error occurs
  '''

  def on_error(self, status):
    print("IN on error")
    # pdb.set_trace()
    print(status)


# creating MainTwitter() class to contain the multiple functions that were spread throughout messy_twitter.py


class TwitterMain():
  # __init__() function sets up authentication and other variables and conn to db
  def __init__(self, conn, num_tweets_to_grab, retweet_count):
    # authentication using unique keys from credentials.py that were taken from apps.twitter.com after app registration.
    self.auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    self.auth.set_access_token(access_token, access_secret)

    self.api = tweepy.API(self.auth)
    self.twit_utils = Twit_utils(self.api)

    self.conn = conn
    self.c = self.conn.cursor()

    self.s = stats()

    self.num_tweets_to_grab = num_tweets_to_grab
    self.retweet_count = retweet_count

  # get_streaming_data() function reads streaming data
  def get_streaming_data(self):
    tweets_grabbed = 0
    while (tweets_grabbed < self.num_tweets_to_grab):
      # create twitter_stream with auth data and the twitter_listener() class. calls twitter_stream_sample() function to get sample of tweets. initializes internal counter. passes in value of number_tweets_to_grab when twitter_listener class created.
      twitterStream = Stream(self.auth, listener(self.s, self.twit_utils, self.num_tweets_to_grab, self.retweet_count))
      try:
        twitterStream.sample()
      except Exception as e:
        print("Error. Restarting Stream.... Error: ")
        print(e.__doc__)
        # print(e.message)
        print("Le Error! Restart")
        time.sleep(3)  # Sleep for 3 minutes if error ocurred
      finally:
        tweets_grabbed = self.s.get_tweets_grabbed()
        print("tweets_grabbed = ", tweets_grabbed)

    # after streaming data is gathered, this reads the data that has been stored
    # get_stats() function returns everything that has been stored
    lang, top_lang, love_words, swear_words, top_tweets, countries = self.s.get_stats()

    print(Counter(lang))
    print(Counter(top_lang))
    print("Love Words {} Swear Words {}".format(love_words, swear_words))
    print(Counter(countries))

    # the get_streaming_data() function gives results from the stats() class and writes them to the database. this occurs after all tweets have been gathered, so the real-time stream script continues to work as anticipated. lang, top_lang, and datetime are added to the db
    # (str(list(Counter(lang).items())) is because python objects can't be stored in a db so these python objects are converted to a counter and then to a string, in the db, the fields will be populated with strings that contain python lists for easy readability
    self.c.execute("INSERT INTO lang_data VALUES (?,?, DATETIME('now'))", (str(list(Counter(lang).items())), str(list(Counter(top_lang).items()))))

    self.c.execute("INSERT INTO love_data VALUES (?,?, DATETIME('now'))", (love_words, swear_words))

    # top_tweets are returned as a list and each one is written to the db. loops over tweets, writing each one + the current time, then commits to the db
    for t in top_tweets:
      self.c.execute("INSERT INTO twitter_data VALUES (?, DATETIME('now'))", (t,))

    self.c.execute("INSERT INTO country_data VALUES (?, DATETIME('now'))", (str(list(Counter(countries).items())),))

    self.conn.commit()

  '''
  # get_trends() function reads trends

  trends_place() function returns the top 50 trending topics where (1) specifies to return global trends. different numbers within the parantheses correspond to different locations where trends may be returned <https://dev.twitter.com/rest/reference/get/trends/place>. examples: trends_place(23424977) = United States. trends_place(7) = San Francisco
  '''

  def get_trends(self):
    # this line excludes trends that have hashtags
    # trends = self.api.trends_place(1, exclude='hashtags')
    trends = self.api.trends_place(1)
    trend_data = []

    # looping over ['trends'] from the JSON list because the trends_place function returned a JSON iterator
    for trend in trends[0]["trends"]:
      # print(trend['name'])
      trend_tweets = []
      trend_tweets.append(trend['name'])
      # returns trend and 3 tweets for each corresponding trend
      tt = tweepy.Cursor(self.api.search, q=trend['name']).items(3)

      # looping over the iterator where the iterator was returned from the term search. prints tweet's text and the number of retweets for the corresponding tweet
      for t in tt:
        tweet_html = self.twit_utils.get_tweet_html(t.id)
        trend_tweets.append(tweet_html)
        # print(tweet_html)

      # tuple created with returned list to allow writing the entire thing as one block into the db
      trend_data.append(tuple(trend_tweets))

    # list format: first entry is trend, the next three are tweets for each corresponding trend
    self.c.executemany("INSERT INTO trend_data VALUES (?,?,?,?, DATETIME('now'))", trend_data)

    self.conn.commit()


# by doing this main check, code only executes when wanting to run the module as a program and not have it execute when someone just wants to import the module and call the functions themselves
if __name__ == "__main__":
  num_tweets_to_grab = 2000
  retweet_count = 30000
  # create connection to twitterlytics_data.db in main code. here, the db is being passed to the MainTwitter() class, but opening and closing it from the main code. this is important because if the class code were to crash, the database may still safely be closed
  try:
    conn = sqlite3.connect(db)
    twit = TwitterMain(conn, num_tweets_to_grab, retweet_count)
    twit.get_streaming_data()
    twit.get_trends()

  except Exception as e:
    print(e.__doc__)

  # if class code crashes, database is still able to be closed safely, thanks to the 'finally' line
  finally:
    conn.close()
