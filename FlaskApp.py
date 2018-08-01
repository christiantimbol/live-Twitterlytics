'''
###################################################################################################################################

FlaskApp.py: front-end built using Flask and connected to twitter.py backend + twitter_data.db (create_database.py)

prior to FlaskApp.py... messy_twitter.py, twitter.py, create_database.py, test_frontend.py, and test_backend.py have been written

to run front-end, input the following into terminal...
> python FlaskApp.py

###################################################################################################################################
'''


from flask import Flask, render_template
import sqlite3
# abstract syntax trees
import ast
from credentials import *

db = "twitterlytics_data.db"

app = Flask(__name__)

# get_top_tweets() function: calling this function to get top_tweets and datetime. datetime is for debugging in order to check if script is running regularly.


def get_top_tweets():
  # open db
  conn = sqlite3.connect(db)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()

  # read last 30 tweets and date-time
  c.execute("SELECT * from twitter_data  ORDER BY datetime DESC LIMIT 30")
  result = c.fetchall()
  tweets = []

  datetime_toptweets = result[0]['datetime']

  for tweet in result:
    tweets.append(tweet['top_tweet'])

  conn.close()

  # results returned to get_top_tweets() function
  return tweets, datetime_toptweets


# get_trends() function: reads last 10 values but each value is comprised of 1 trend and 3 tweets corresponding to that trend

def get_trends():
  conn = sqlite3.connect(db)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()

  trend = []
  trend_tweet = []

  c.execute("SELECT * from trend_data ORDER BY datetime DESC LIMIT 10")
  result = c.fetchall()

  datetime_trends = result[0]['datetime']

  for r in result:
    trend.append(r['trend'])
    trend_tweet.append(r['trend_id1'])
    trend_tweet.append(r['trend_id2'])
    trend_tweet.append(r['trend_id3'])

  conn.close()

  # returns trend list and trend_tweet list which is comprised of trending tweets
  return trend, trend_tweet, datetime_trends


# get_lang() function: reads language data but only reading one value because data is in an [array]. SqLite cannot store Python lists so the list was converted to a string in twitter.py. main() function (next code block) converts the string to a list and returns it

def read_data():

  conn = sqlite3.connect(db)
  conn.row_factory = sqlite3.Row
  c = conn.cursor()
  c.execute("SELECT * from lang_data ORDER BY datetime DESC LIMIT 1")

  result = c.fetchone()
  lang = ast.literal_eval(result['language'])
  top_lang = ast.literal_eval(result['top_language'])

  c.execute("SELECT * from love_data ORDER BY datetime DESC LIMIT 1")

  result = c.fetchone()
  love_words = result['love_words']
  swear_words = result['swear_words']

  c.execute("SELECT * from country_data ORDER BY datetime DESC LIMIT 1")

  result = c.fetchone()
  country = ast.literal_eval(result['country'])
  datetime = result['datetime']

  conn.close()

  return lang, top_lang, love_words, swear_words, country, datetime


@app.route("/")
def main():

  tweets, datetime_toptweets = get_top_tweets()
  language_data = []
  top_language_data = []
  words_data = []
  country_data = []

  lang, top_lang, love_words, swear_words, country, datetime = read_data()
  for l in lang:
    language_data.append([l[0], l[1], l[1]])

  for t in top_lang:
    top_language_data.append([t[0], t[1], t[1]])

  words_data.append(['love_words', love_words, love_words])
  words_data.append(['swear_words', swear_words, swear_words])

  country_data.append(['Country', 'Popularity'])

  for coun in country:
    country_data.append([coun[0], coun[1]])

  return render_template('analysis.html', language_data=language_data, top_language_data=top_language_data, words_data=words_data, country_data=country_data, datetime=datetime, tweets=tweets, datetime_toptweets=datetime_toptweets)


if __name__ == "__main__":
  app.run(debug=True)
