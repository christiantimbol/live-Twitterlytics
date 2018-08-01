'''
###################################################################################################################################

test_backend.py: back-end tests (written after back-end has been written)

prior to test_backend.py... messy_twitter.py, twitter.py, create_database.py, and test_frontend.py have been written

for test-building...
  on this page, the users expect to see:
    1) graphs with languages and top languages statistics
    2) top tweets
    3) twitter trends

  despite 1-3 being webserver tests, they affect the backend since the backend produces the stats, thus the tests will not to be reconfigured and ran for the backend

###################################################################################################################################
'''
# initial imports
import unittest
import sqlite3
from twitter import *
import pdb
import ast
import warnings
warnings.simplefilter("ignore", ResourceWarning)

# creating TestTwit() class using Python Unittest library to encompass all back-end test functions


class TestTwit(unittest.TestCase):
  # before running any tests, setUp() function is called
  def setUp(self):
    # creating sqlite db in memory to test db code without wrecking live db
    self.conn = sqlite3.connect(":memory:")
    c = self.conn.cursor()
    # create tables to reflect db created in create_database.py
    cmd = "CREATE TABLE trend_data (trend TEXT, trend_id1 TEXT, trend_id2 TEXT, trend_id3 TEXT, datetime TEXT)"
    c.execute(cmd)

    cmd = "CREATE TABLE twitter_data (top_tweet TEXT, datetime TEXT)"
    c.execute(cmd)

    cmd = "CREATE TABLE lang_data (language TEXT, top_language TEXT, datetime TEXT)"
    c.execute(cmd)

    cmd = "CREATE TABLE love_data (love_words INT, swear_words INT, datetime TEXT)"
    c.execute(cmd)

    cmd = "CREATE TABLE country_data (country TEXT, datetime TEXT)"
    c.execute(cmd)

    self.conn.commit()
    # creating MainTwitter() class reflected from twitter.py. only grabbing 5 tweets for fast testing
    num_tweets_to_grab = 5
    retweet_count = 0
    self.twit = TwitterMain(self.conn, num_tweets_to_grab, retweet_count)

  # test_streaming_data() function is a feature test. calls twit.get_streaming_data() function from twitter.py to gather tweets and check if tweets have been written to db. does not check actual content since content is unpredictable depending on when the data was pulled using the Streaming API. as long as content is written to db, test passes.
  def test_streaming_data(self):
    self.twit.get_streaming_data()
    try:
      lang, top_lang, love_words, swear_words, country = self.read_data()
    except:
      self.fail("test_streaming_data: Nothing written to database. Test Failed.")

  # test_trends() function is a feature test. calls twit.get_trends() function from twitter.py to gather trends and check if trends have been written to db. does not check actual content since content is unpredictable depending on when the data was pulled using the Streaming API. as long as content is written to db, test passes.
  def test_trends(self):
    self.twit.get_trends()
    try:
      trend, trend_tweet = self.get_trends()
    except:
      self.fail("test_trends: Nothing written to database. Test Failed.")

  # test_stats() function tests to ensure stats() class code from twitter.py has no bugs. test_stats() function writes data and reads it back
  def test_stats(self):
    s = stats()
    s.add_lang("English")
    s.add_top_lang("Wooki")
    s.love_word_found()
    s.love_word_found()
    s.swear_word_found()
    s.save_top_tweets("Tweet")
    s.add_country("Tatooine")

    lang, top_lang, love_words, swear_words, top_tweets, countries = s.get_stats()

    self.assertEqual(lang[0], "English")
    self.assertEqual(top_lang[0], "Wooki")
    self.assertEqual(love_words, 2)
    self.assertEqual(swear_words, 1)
    self.assertEqual(top_tweets[0], "Tweet")
    self.assertEqual(countries[0], "Tatooine")

  # read_data() function is a helper function to read data from db
  def read_data(self):
    # taken from FlaskApp.py because it is a common test function and allows keeping the tests independent of the code

    self.conn.row_factory = sqlite3.Row
    c = self.conn.cursor()
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

    return lang, top_lang, love_words, swear_words, country

  # get_trends() function is a helper function to read data from db
  def get_trends(self):
    self.conn.row_factory = sqlite3.Row
    c = self.conn.cursor()

    trend = []
    trend_tweet = []

    c.execute("SELECT * from trend_data ORDER BY datetime DESC LIMIT 5")
    result = c.fetchall()

    for r in result:
      trend.append(r['trend'])
      trend_tweet.append(r['trend_id1'])
      trend_tweet.append(r['trend_id2'])
      trend_tweet.append(r['trend_id3'])

    return trend, trend_tweet

  # tearDown() function is to tear down memory db at end of back-end tests
  def tearDown(self):
    self.conn.close()


if __name__ == "__main__":
  unittest.main(warnings='ignore')
