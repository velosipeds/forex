import time
import sqlalchemy
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.dialects.mysql import LONGTEXT
import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import urllib2
import urllib
import json
import pprint
import dateutil.parser
import gevent
import datetime
import tweepy
import sys

print_sql_queries = False
articles_per_page = 100

Base = declarative_base()
mysql_url = "mysql://zplizzi:yummy4money@twitter.c2ggnaqt6wye.us-west-1.rds.amazonaws.com/twitter?charset=utf8&use_unicode=1"
sqlite_url = 'sqlite:///database.db'
local_mysql_url = "mysql://root:yummy4money@127.0.0.1/twitter?charset=utf8&use_unicode=1"
db = create_engine(local_mysql_url, echo=print_sql_queries, encoding='utf-8')
session = sessionmaker()
session.configure(bind=db)
session = session()

db.engine.execute("SET NAMES 'utf8'; SET CHARACTER SET utf8;")

class Tweet(Base):
	__tablename__ = "tweets"
	
	tweet_id = Column(String(25), primary_key = True)
	twitter_user_id = Column(String(25))
	timestamp = Column(DateTime)
	language = Column(String(10))
	retweeted_status_id = Column(String(25))
	reply_to_id = Column(String(25))
	favorite_count = Column(Integer)
	retweet_count = Column(Integer)
	latitude = Column(Numeric(12, 8))
	longitude = Column(Numeric(12, 8))
	text = Column(String(200))
	
	def __init__(self, tweet_id, twitter_user_id, timestamp, language, retweeted_status_id, reply_to_id, \
	favorite_count, retweet_count, latitude, longitude, text):
		self.tweet_id = tweet_id
		self.twitter_user_id = twitter_user_id
		self.timestamp = timestamp
		self.language = language
		self.retweeted_status_id = retweeted_status_id
		self.reply_to_id = reply_to_id
		self.favorite_count = favorite_count
		self.retweet_count = retweet_count
		self.latitude = latitude
		self.longitude = longitude
		self.text = text
	
class Hashtag(Base):
	__tablename__ = "hashtags"
	
	tweet_id = Column(String(25), primary_key = True)
	hashtag = Column(String(200), primary_key = True)

	def __init__(self, tweet_id, hashtag):
		self.tweet_id = tweet_id
		self.hashtag = hashtag
		
	
class User(Base):
	__tablename__ = "twitter_users"
	
	twitter_user_id = Column(String(25), primary_key = True)
	
	created_timestamp = Column(DateTime)
	default_profile_image = Column(Boolean)
	description = Column(String(300))
	favourites_count = Column(Integer)
	followers_count = Column(Integer)
	friends_count = Column(Integer)
	language = Column(String(10))
	location = Column(String(200))
	name = Column(String(100))
	screen_name = Column(String(30))
	statuses_count = Column(Integer)
	time_zone = Column(String(100))
	verified = Column(Boolean)

	def __init__(self, twitter_user_id, created_timestamp, default_profile_image, description, favourites_count, \
	followers_count, friends_count, language, location, name, screen_name, statuses_count, time_zone, verified):
		self.twitter_user_id = twitter_user_id
		self.created_timestamp = created_timestamp
		self.default_profile_image = default_profile_image
		self.description = description
		self.favourites_count = favourites_count
		self.followers_count = followers_count
		self.friends_count = friends_count
		self.language = language
		self.location = location
		self.name = name
		self.screen_name = screen_name
		self.statuses_count = statuses_count
		self.time_zone = time_zone
		self.verified = verified
		
		
	
Base.metadata.create_all(db)

last_sql = " "

from textwrap import TextWrapper
class StreamWatcherListener(tweepy.StreamListener):
	last_sql = ""
	i = 0

	def on_status(self, status):
		self.i += 1
		try:
			print (status.created_at - datetime.datetime.now()).seconds - 86384
			
			tweet_obj = Tweet(	status.id_str, 
								status.user.id_str,
								status.created_at,
								status.lang,
								status.retweeted_status.id_str if hasattr(status, 'retweeted_status') else None,
								status.in_reply_to_status_id_str,
								status.favorite_count,
								status.retweet_count,
								status.coordinates["coordinates"][0] if status.coordinates is not None and "coordinates" in status.coordinates else None,
								status.coordinates["coordinates"][1] if status.coordinates is not None and "coordinates" in status.coordinates else None,
								status.text
								)
			session.add(tweet_obj)
			#session.flush()
			
			#print status.text
			
			#print type(status.user.verified)
			
			format_string = (status.user.id,
						status.user.created_at,
						status.user.default_profile_image,
						status.user.description.replace("%", "").encode('utf-8').decode('utf-8').replace("\\", "").replace(":", "") if status.user.description else None,
						status.user.favourites_count,
						status.user.followers_count,
						status.user.friends_count,
						status.user.lang,
						status.user.location.replace("%", "").encode('utf-8').decode('utf-8').replace("\\", "").replace(":", "") if status.user.location else None,
						status.user.name.replace("%", "").encode('utf-8').decode('utf-8').replace("\\", "").replace(":", "") if status.user.name else None,
						status.user.screen_name.replace("%", "").encode('utf-8').decode('utf-8').replace("\\", "") if status.user.screen_name else None,
						status.user.statuses_count,
						status.user.time_zone,
						1 if status.user.verified == True else 0)
						#status.user.verified)d
						
		
		
		

			#print "format string"
			#print format_string
			query = """REPLACE twitter_users values (%s, "%s", %s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % format_string
			self.last_sql = query
			session.execute(query)

			#session.add(user_obj)
			if self.i % 50 == 0:
				session.commit()
				self.i == 0
				
		except:
			print "failed inserting tweet"
			print "Unexpected error:", sys.exc_info()
			print self.last_sql
			session.rollback()
			

	def on_error(self, status_code):
		print 'An error has occured! Status code = %s' % status_code
		return True  # keep stream alive

	def on_timeout(self):
		print 'Snoozing Zzzzzz'


consumer_key = "GfqAfMzJhKFGGDOEfwguxWm7W"
consumer_secret = "RJMr1p50oWPE1Z7r04PxBCQUyVyzGotyeOu0W50YjJ6tEdE7ev"
access_token = "342987024-JqRfvDSpcRizGY8oUNkuKSw6NiJCg934if4AjDiG"
access_token_secret = "DuHEbWCbvTt1YeBrEvIrTyBOWFFCQy6OOfrRcXJVNKAWF"


import tweepy

listener = StreamWatcherListener()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def stream_data():
	stream = tweepy.Stream(auth, listener, timeout=None)
	stream.sample()
	try:
		stream = tweepy.Stream(auth, listener, timeout=None)
		stream.sample()
	except:
		print "streaming failed, trying again"
		time.sleep(10)
		stream_data()

stream_data()
