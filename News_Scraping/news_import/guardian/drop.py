#python
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
drop_old_tables = True



Base = declarative_base()
mysql_url = "mysql://forex:yummy4money@zplizzi.cddqdipecvfk.us-west-2.rds.amazonaws.com/forex?charset=utf8"
sqlite_url = 'sqlite:///database.db'
db = create_engine(mysql_url, echo=print_sql_queries)
session = sessionmaker()
session.configure(bind=db)
session = session()

if drop_old_tables:
	db.engine.execute("drop table if exists articles")
	db.engine.execute("drop table if exists tags")
