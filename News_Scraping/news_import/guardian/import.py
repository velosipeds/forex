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



Base = declarative_base()
mysql_url = "mysql://forex:yummy4money@zplizzi.cddqdipecvfk.us-west-2.rds.amazonaws.com/forex"
sqlite_url = 'sqlite:///database.db'
db = create_engine(mysql_url, echo=print_sql_queries)
session = sessionmaker()
session.configure(bind=db)
session = session()


class Article(Base):
    __tablename__ = "articles"
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
    __tablename__ = "tags"
    category = Column(String(80))
    article_id = Column(Integer, primary_key = True)
    section = Column(String(200), primary_key = True)

    def __init__(self, category, article_id, section):
        self.category = category
        self.article_id = article_id
        self.section = section    
    
Base.metadata.create_all(db)





#for i in range(1, 100):

def get_page(i):

	page = i
	print i

	time.sleep(.3)

	url = "http://content.guardianapis.com/search?order-by=newest&use-date=published&show-tags=keyword&show-fields=all&page=%i&page-size=%i&q=world&api-key=xdxfyey39tqhn2mwgmfdjxtj" % (page, articles_per_page)

	#print url

	req = urllib2.Request(url=url)

	f = urllib2.urlopen(req)

	data = json.loads(f.read())


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

	session.commit()

for j in range(0, 500):

	threads = []
	for i in range(1, 10):
		threads.append(gevent.spawn(get_page, j*10 + i))


	#threads = [gevent.spawn(get_page, page) for page in xrange(1, 100)]
	gevent.joinall(threads)
