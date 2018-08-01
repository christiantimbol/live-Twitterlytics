'''

messy_twitter.py

this file has code spread all over, such as in the class, some just being run in the __main__ section, etc which makes it hard to test. ToDo = clean this up.

1) how to manage the code?
2) how to return the data collected in twitter_listener class into the __main__ code?

'''

'''
before beginning, ensure to input the following into the terminal after activating a virtual enviroment:

> pip install -r requirements.txt

'''


'''
imports tweepy, tweepy streaming API that continuously reads data from Twitter (10% of live tweets), file that contains unique twitter application passwords, python debugger
'''

import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
from credentials import *
import pdb
import json
from collections import Counter

'''
Twitter's JSON object returns languages as a 2-character code under the lang json key, so this 'langs' python dictionary will convert the 2-char code to the corresponding language name
'''

langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}

'''
defined twitter_listener class, inherited from Tweepy's StreamListener. 2 necessary functions for this class are: on_data() and on_error()
'''


class twitter_listener(StreamListener):

  '''
  adding a counter to make code stop since code keeps running until killed in terminal with Ctrl+C. counter can not be added to on_data() because on_data() is newly called every time. so, counter is added to twitter_listener class during initialization function __init__() so the counter will be available each time on_data() is called
  '''

  '''
  __init__() function called when twitter_listener class created. passing in number_tweets_to_grab variable. internal counter is initialized in main code.
  '''

  '''
  top tweets defined as tweets that exceed 10,000 retweets. added retweet_count parameter to __init__() function, initialized by quantification of what constitutes a top tweet. this quantification may be changed according to subjective definition of top tweet.
  '''

  def __init__(self, number_tweets_to_grab, retweet_count=10000):
    self.counter = 0
    self.number_tweets_to_grab = number_tweets_to_grab
    self.retweet_count = retweet_count
    # after python dictionary converts the 2-char lang into the corresponding language, the languages need to be stored, so self.languages variable is added to the __init__ function
    self.languages = []
    self.top_languages = []

  '''
  on_data() function tells Tweepy what to do when new Tweet is available. in this case, on_data() loads json data using the inbuilt json library and prints the text of the tweets.
  '''

  def on_data(self, data):
    try:
      json_data = json.loads(data)
      '''
      uncomment for test to check if json_data is received
      # print(json_data['text'])
      '''
      # stores converted languages corresponding to each tweet that is returned
      self.languages.append(langs[json_data['lang']])

      self.counter += 1
      # gets retweet_count by parsing the Twitter json object
      retweet_count = json_data['retweeted_status']['retweet_count']

      '''
      check if tweet's retweet_count is greater than retweet_count for self-defined top tweet (>=10000). if passes, prints its text, retweet_count, and lang, then saves language.

      # ToDo '@2': see if i can add code to retweet the tweet if it's a top tweet
      '''
      if retweet_count >= self.retweet_count:
        print(json_data['text'], retweet_count, langs[json_data['lang']])
        print('^this tweet IS a top tweet')
        self.top_languages.append(langs[json_data['lang']])

      '''
      ++1: was initially confused why counter was incrementing despite printed tweets not adding up to the counter amount, but the code only printed tweets > 10000 retweets. with this additional if statement, the non-top_tweet still prints in the console, but that data doesnt save. prevents further confusion regarding the incrementing counter with non-matching printed tweets in the terminal
      '''
      if retweet_count < self.retweet_count:
        print(json_data['text'], retweet_count, langs[json_data['lang']])
        print('^this tweet IS NOT a top tweet')

      if self.counter >= self.number_tweets_to_grab:
        # after appending the converted languages, print the languages that were returned. counter() function counts each object in the list corresponding to the number of tweets in that language
        print(self.languages)  # prints all languages from the number_tweets_to_grab
        print(self.top_languages)  # prints language most present in the number_tweets_to_grab
        print(Counter(self.languages))  # prints number of tweets per languages
        print(Counter(self.top_languages))  # prints top language
        # returning false causes class to exit after reaching the specified number_tweets_to_grab (which is how Tweepy internally works).
        return False

      return True
    except:
      # !!!ToDo: see comment '@1'
      pass
      print('== passed tweet')
      '''
      ToDo: '+1' is the unicode problem in terminal the reason why the terminal is not printing the defined number_tweets_to_grab? sometimes it does, and sometimes it does not. i know how many tweets it's grabbing because of printing 'passed tweet'. check '+1' in bugs.txt for more info.

      the counter still increments accordingly, but the terminal is not printing specific number_tweets_to_grab despite the terminal displaying the langs used and the number of tweets per lang

      screenshot of '+1' on desktop

      UPDATE: added another if statement (see '++1') and the counter includes tweets that are less than 10000, but doesnt display the json data if the tweet is less than 10000. added code so now it displays tweets despite not being a top_tweet

      !!!ANOTHER UPDATE: terminal is not matching number_tweets_to_grab (exceeds it). ex: parameter is set to two, but code passes 4 tweets ('== passed tweet') and prints the JSON of a tweet, whether it's a top tweet or not. counter still adds to 10 despite printing more than ten tweets (passed, top, and non_top)
      '''

  '''
  attempted to fix receiving broken (deleted/strangely-formatted) tweets because without the previous lines (try: ... except: pass), run-time error occurs because of receiving broken tweets. now, if the code finds broken json data, it prints '== passed tweet' and moves on.

  @1: DANGEROUS because instead of fixing problem, problems are just hidden. bad tweets along with bugs in the code will just be hidden.
  '''

  '''
  on_error() function prints error status if error occurs
  '''

  def on_error(self, status):
    print(status)


'''
by doing this main check, code only executes when wanting to run the module as a program and not have it execute when someone just wants to import the module and call the functions themselves
'''
if __name__ == '__main__':

  '''
  authentication using unique keys from credentials.py that were taken from apps.twitter.com after app registration.
  '''
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)
  twitter_api = tweepy.API(auth)

  '''
  term search where q='search_term' and (_) in items(_) returns specified number of results
  '''
  search_results = tweepy.Cursor(twitter_api.search, q='python').items(1)

  '''
  looping over the iterator where the iterator was returned from the term search. prints tweet's text and the number of retweets for the corresponding tweet
  '''
  for result in search_results:
    print('result from search_result:')
    print(result.text)
    print(result.retweet_count)

  '''
  trends_place() function returns the top 50 trending topics where (1) specifies to return global trends. different numbers within the parantheses correspond to different locations where trends may be returned <https://dev.twitter.com/rest/reference/get/trends/place>. examples: trends_place(23424977) = United States. trends_place(7) = San Francisco

  # this line excludes trends that have hashtags
  trends = twitter_api.trends_place(1, exclude='hashtags')
  '''
  trends = twitter_api.trends_place(1)

  '''
  looping over ['trends'] from the JSON list because the trends_place function returned a JSON iterator
  '''
  for trend in trends[0]['trends']:
    '''
    # returns a messy JSON list
    print(trends[0]['trends'])
    # returns a less messy JSON list
    print(trends[0]['trends'][0])
    '''
    # returns a clean list of the trend names from the JSON list
    print(trend['name'])

  '''
  create twitter_stream with auth data and the twitter_listener() class. calls twitter_stream_sample() function to get sample of tweets. initializes internal counter. passes in value of number_tweets_to_grab when twitter_listener class created.
  '''
  twitter_stream = Stream(auth, twitter_listener(number_tweets_to_grab=10))
  try:
    twitter_stream.sample()
  except Exception as e:
    print(e.__doc__)
