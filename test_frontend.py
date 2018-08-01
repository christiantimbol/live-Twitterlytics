'''
###################################################################################################################################

test_frontend.py: front-end tests (written before front-end is written)

prior to test_frontend.py, messy_twitter.py, twitter.py and create_database.py have been written

for test-building...
  on this page, the users expect to see:
    1) graphs with languages and top languages statistics
    2) top tweets
    3) twitter trends

using Selenium with Unittest:
  - Selenium is a tool to automate the browser

  to install...
  > brew install selenium-server-standalone

  to run...
  > selenium-server -port 4444

  for options...
  > selenium-server -help

###################################################################################################################################
'''

# initial imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import sqlite3
import requests

# creating TestFlask() class to encompass all front-end test functions


class TestFlask(unittest.TestCase):

  # test_web_app_running() function: first test which checks if webserver is running. minor changes may kill webapp, so first test is to check if server is running. if test can not find running server at http://127.0.0.1:5000/ (development server), it will exit
  # !!!ToDo: check > selenium-server -port 4444 with > selenium-server -port 5000
  def test_web_app_running(self):
    try:
      r = requests.get('http://127.0.0.1:5000/')
    except:
      self.fail('TEST 1.1 FAILED: Unable to open webapp. Server not running or crashed.')

  # test_lang() function: obtain webserver page, search the page for the text 'most used languages ...' and if it is not found, test fails. this test verifies that webapp is up and running and receives/displays data from twitterlytics_data.db
  def test_lang(self):

    r = requests.get('http://127.0.0.1:5000/')
    page_src = r.text

    if page_src.find('Most used languages on Twitter: All Tweets') < 0:
      self.fail('TEST 2.1 FAILED: Cannot find most common languages')

  # test_top_tweets() function: similar to test_lang() function, this function searches for 'Most Popular Tweets'. an extra search for 'blockquote class...' is included because embedded tweets start with that HTML code. so this test looks for embedded tweets and text being displayed on the page
  def test_top_tweets(self):
    r = requests.get('http://127.0.0.1:5000/top_tweets')
    page_src = r.text

    if page_src.find('Most Popular Tweets') < 0:
      self.fail('TEST 3.1 FAILED: Top tweets failed')

    if page_src.find('<blockquote class="twitter-tweet') < 0:
      self.fail('TEST 3.2 FAILED: Cannot find embedded top tweets')

  # test_trends() function: similar to TEST 2.1, 3.1, and 3.2. refer to those comments for more information
  def test_trends(self):
    r = requests.get('http://127.0.0.1:5000/trends')
    page_src = r.text

    if page_src.find('Trending On Twitter:') < 0:
      self.fail('TEST 4.1 FAILED: Trends failed')

    if page_src.find('<blockquote class="twitter-tweet"') < 0:
      self.fail('TEST 4.2 FAILED: Cannot find the trending tweets')


if __name__ == '__main__':
  unittest.main(warnings='ignore', failfast=True)
