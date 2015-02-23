import gevent.monkey
gevent.monkey.patch_socket()

import time
import sqlalchemy
from sqlalchemy import *
from sqlalchemy import event
import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import urllib2
import urllib
import json
import pprint
import dateutil.parser
import gevent

print_sql_queries = False
articles_per_page = 100	


Base = declarative_base()
#database_url = 
db = create_engine('sqlite:///database.db', echo=print_sql_queries)
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
    section_id = Column(String(20))
    body = Column(Text)
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
    category = Column(String(30))
    article_id = Column(Integer, primary_key = True)
    section = Column(String(30), primary_key = True)

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

	print url

	req = urllib2.Request(url=url)

	f = urllib2.urlopen(req)

	data = json.loads(f.read())


	for article in data["response"]["results"]:
	    #print article["fields"]["body"]
	    try:    
		article_obj = Article(article["id"],
		                    article["webTitle"],
		                    article["apiUrl"],
		                    article["webUrl"],
		                    article["sectionId"],
		                    article["fields"]["body"],
		                    dateutil.parser.parse(article["webPublicationDate"]),
		                    article["fields"]["trailText"],
		                    article["fields"]["wordcount"])
		session.add(article_obj)
		session.flush()
		for tag in article["tags"]:
		    tag_obj = Tag(tag["sectionId"], tag["id"], article_obj.article_id)
		    session.add(tag_obj)    

	    except:
		print "article failed to parse"

	session.commit()

for j in range(0, 20):

	threads = []
	for i in range(1, 10):
		threads.append(gevent.spawn(get_page, j*10 + i))


	#threads = [gevent.spawn(get_page, page) for page in xrange(1, 100)]
	gevent.joinall(threads)
