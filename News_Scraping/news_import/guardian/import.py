import gevent.monkey
gevent.monkey.patch_socket()

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

print_sql_queries = False
articles_per_page = 100

key1 = "4xwpp7jnhw4veahnrkg38pgx"
key2 = "xdxfyey39tqhn2mwgmfdjxtj"
key3 = "z7ps6r8aqsh59w8rqqtdbfpk"
key4 = "535wcthj4zjcy5vjdzp9mygb"
key5 = "ksbea5drekrzsv9vngj94ax3"
key6 = "yfjnkpwet4z3q587xeq36t3x"
key7 = "2ajzjvugxuumevhj2y7xbwy9"

key = key2
result_page_start = 250
result_page_end = 500

Base = declarative_base()
mysql_url = "mysql://forex:yummy4money@forex.c2ggnaqt6wye.us-west-1.rds.amazonaws.com/forex"
sqlite_url = 'sqlite:///database.db'
db = create_engine(mysql_url, echo=print_sql_queries)
session = sessionmaker()
session.configure(bind=db)
session = session()


class Article(Base):
	__tablename__ = "articles_new"
	article_id = Column(Integer, autoincrement=True, primary_key = True)
	web_id = Column(String(150))
	title = Column(String(200))
	api_url = Column(String(300))
	web_url = Column(String(300))
	section_id = Column(String(80))
	body = Column(LONGTEXT)
	pub_date = Column(DateTime)
	subtitle = Column(Text)
	wordcount = Column(Integer)
	   
	def __init__(self, web_id, title, api_url, web_url, 
			section_id, body, pub_date, subtitle, wordcount):
		self.web_id = web_id
		self.title = title
		self.api_url = api_url
		self.web_url = web_url
		self.section_id = section_id
		self.body = body
		self.pub_date = pub_date
		self.subtitle = subtitle
		self.wordcount = wordcount
	
	
class Tag(Base):
	__tablename__ = "tags_new"
	category = Column(String(80))
	article_id = Column(Integer, primary_key = True)
	section = Column(String(200), primary_key = True)

	def __init__(self, category, article_id, section):
		self.category = category
		self.article_id = article_id
		self.section = section	
	
Base.metadata.create_all(db)



section = "world"

#for i in range(1, 100):
pp = pprint.PrettyPrinter(indent=4)

def get_page(i):

	page = i
	print i
	
	time.sleep(.25)

	url = "http://content.guardianapis.com/search?order-by=newest&use-date=published&show-tags=keyword&show-fields=all&page=%i&page-size=%i&api-key=%s" % (page, articles_per_page, key)

	#print url

	try:
		req = urllib2.Request(url=url)
		f = urllib2.urlopen(req)
		data = json.loads(f.read())
	except Exception as e:
		print "HTTP request error at page %i" % page
		print e

	for article in data["response"]["results"]:
		try:
			article_obj = Article(article["id"],
					article["webTitle"].encode('latin-1', 'ignore'),
					article["apiUrl"].encode('latin-1', 'ignore'),
					article["webUrl"].encode('latin-1', 'ignore'),
					article["sectionId"].encode('latin-1', 'ignore'),
					article["fields"]["body"].encode('latin-1', 'ignore'),
					dateutil.parser.parse(article["webPublicationDate"]).replace(tzinfo=None),
					article["fields"]["trailText"].encode('latin-1', 'ignore'),
					article["fields"]["wordcount"])
			session.add(article_obj)
			session.flush()
			for tag in article["tags"]:
				tag_obj = Tag(tag["sectionId"], article_obj.article_id, tag["id"])
				session.add(tag_obj)	

		except:
			print "article failed to parse"
			#pp.pprint(article)

	session.commit()

	
for j in range(result_page_start, result_page_end):
	threads = []
	for i in range(1, 10):
		threads.append(gevent.spawn(get_page, j*10 + i))
	gevent.joinall(threads)
