# run this file in terminal to create database in "DB Browser for SQLite"

# opening database and connecting to it. Sqlite3 automatically creates the database if it doesn't exist
import sqlite3

db = "twitterlytics_data.db"

conn = sqlite3.connect(db)
c = conn.cursor()

try:
  c.execute("drop table trend_data")
  c.execute("drop table twitter_data")
  c.execute("drop table lang_data")
  c.execute("drop table love_data")
  c.execute("drop table country_data")
except:
  # do nothing if there's nothing to drop
  pass

# using SQL data to create trend_data table
cmd = "CREATE TABLE trend_data (trend TEXT, trend_id1 TEXT, trend_id2 TEXT, trend_id3 TEXT, datetime TEXT)"
c.execute(cmd)

# using SQL data to create twitter_data table
cmd = "CREATE TABLE twitter_data (top_tweet TEXT, datetime TEXT)"
c.execute(cmd)

# using SQL data to create lang_data table that contains 3 fields. language TEXT and top_language TEXT are obtained from twitter.py. datetime TEXT is stored so SQL commands such as getting all tweets in last day may be done
cmd = "CREATE TABLE lang_data (language TEXT, top_language TEXT, datetime TEXT)"
c.execute(cmd)

cmd = "CREATE TABLE love_data (love_words INT, swear_words INT, datetime TEXT)"
c.execute(cmd)

cmd = "CREATE TABLE country_data (country TEXT, datetime TEXT)"
c.execute(cmd)

conn.commit()

conn.close()
