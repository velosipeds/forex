import glob
import pybrain
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import matplotlib.pyplot as plt
import datetime
import random
import ast
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
import glob
import pprint
import dateutil.parser
import pprint
import re
from sklearn import linear_model, datasets
import time
from sklearn.naive_bayes import GaussianNB
import nltk
from collections import defaultdict
from sklearn import svm
import pickle
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash

tree = lambda: defaultdict(tree)
dct = tree()

app = Flask(__name__)
app.config.from_object(__name__)

alls = {}
sortedKeys = []
cache = {}
count = 0

tree = lambda: defaultdict(tree)
dct = tree()
n = pickle.load(open('network.pkl', 'rb'))



def mean(l):
	return sum(l)/float(len(l))

def moving_average(delta, data, date):
	# print "MOVING AVG"
#     date = date - delta
	kys = sortedKeys
#     print kys
	i1, i2 = 1, 1
	# print "HERE"
#     print delta.hours
	try:
		d1 = closest_date(date)
		i1 = cache[d1]
	except:
		count = 0
		for k in kys:
	#       print k
			if k > date:
				i1 = count
				break   
		count += 1
	# print "HERE2"
	try:
		d2 = closest_date(date - delta)
		i2 = cache[d2]
	except:
		count = 0
		for k in kys:
	#       print k
			if k > date - delta:
				i2 = count
				break   
			count += 1#     print d1, d2
	points = []
	# print "HERE3"
	#compute avg approx for speed
	datapoints = 5
	ptz = []
	if abs(i1-i2)/5 == 0:
		return mean([float(alls[kys[i1]]), float(alls[kys[i2]])])
	for z in range(i1, i2, abs(i1-i2)/5):
		# print z
		ptz.append(float(alls[kys[z]]))
	return mean(ptz)
	


def get_past_averages(date, dct):
	vec = []
	for back in [1/24.0,.25,1,3,7,31,90,180,365]:

#         if back < 1:    
#             dlt = datetime.timedelta(hours=back*24)

#             vec.append(moving_average_hours(dlt, dct, date))
#         else:
		dlt = datetime.timedelta(days=back)
		# print back
		vec.append(moving_average(dlt, dct, date))
	return vec

def closest_datapoint(d):
	closest =  dct[d.year][d.month][d.day][d.hour][d.minute]
	if str(type(closest)) != "<type 'collections.defaultdict'>":
		return closest
	else:
		return closest_datapoint(d + datetime.timedelta(seconds=60))

def closest_date(d):
	closest =  dct[d.year][d.month][d.day][d.hour][d.minute]
	if str(type(closest)) != "<type 'collections.defaultdict'>":
		return datetime.datetime(d.year,d.month,d.day,d.hour,d.minute)
	else:
		return closest_date(d + datetime.timedelta(seconds=120))

@app.route('/tick', methods=['POST'])
def new_point():
	global alls, sortedKeys, cache

	# sortedKeys = sorted(alls.keys())
	# count = 0
	# for k in sortedKeys:
	#     cache[k] = count
	#     count += 1
	j = request.json
	year = j['year']
	month = j['month']
	day = j['day']
	hour = j['hour']
	minute = j['minute']
	curs = j['rate'][0]
	rate = j['rate'][1]
	dct[year][month][day][hour][minute][curs] = rate
	# print 'here2'

	dt = datetime.datetime(year, month, day, hour, minute)

	alls[dt] = rate
	# print get_past_averages(dt, dct)

	return "Ok"

@app.route('/predict', methods=['POST'])
def predict():
	global alls, sortedKeys, cache

	sortedKeys = sorted(alls.keys())
	count = 0
	for k in sortedKeys:
	    cache[k] = count
	    count += 1
	j = request.json
	year = j['year']
	month = j['month']
	day = j['day']
	hour = j['hour']
	minute = j['minute']
	curs = j['rate'][0]
	rate = j['rate'][1]
	dct[year][month][day][hour][minute][curs] = rate
	# print 'here2'

	dt = datetime.datetime(year, month, day, hour, minute)
	# print 'here3'

	alls[dt] = rate
	z = get_past_averages(dt, dct)
	values = n.activate(z)
	# print values[0]
	# print ','.join([f for f in values])

	return str(values[0]) #half hour


if __name__ == '__main__':
	app.run()