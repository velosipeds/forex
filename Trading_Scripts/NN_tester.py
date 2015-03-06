
# coding: utf-8

# In[187]:

import glob
import pybrain
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import matplotlib.pyplot as plt
import datetime
# get_ipython().magic(u'matplotlib inline')
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
pp = pprint.PrettyPrinter(indent=4)


# In[188]:

def mean(l):
    return sum(l)/float(len(l))


# In[189]:

n = FeedForwardNetwork()
inLayer = LinearLayer(9)
hiddenLayer = SigmoidLayer(18)
outLayer = LinearLayer(3)
n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addOutputModule(outLayer)
in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)

n.addConnection(in_to_hidden)
n.addConnection(hidden_to_out)

n.sortModules()


# In[190]:

trainfile = open('../usd_eur_trainingdata.csv', 'r')
testfile = open('../usd_eur_testingdata.csv', 'r')

train, test = [], []
for line in trainfile:
    line = line.strip().split(',')
    features = line[:-3]
    outputs = line[-3:]
    train.append([features, outputs])

for line in testfile:
    line = line.strip().split(',')
    features = line[:-3]
    outputs = line[-3:]
    test.append([features, outputs])


# In[191]:

ds = SupervisedDataSet(9, 3)
for t in train:
    ds.addSample(t[0], t[1])
print "Dataset of " + str(len(ds)) + " samples."
print "Test set of " + str(len(test)) + " samples."


# In[192]:

# alls = {}

# for fl in glob.glob('../Forex_Data/EURO_USD/*/*.csv')[8:13]:
#     print fl
#     for line in open(fl):
#         line = line.strip('\n').split(' ')
#         date = line[0]
#         rest  = line[1].split(';')
#         time = rest[0]
#         ask = rest[1]
        
#         d = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8]), int(time[:2]), int(time[2:4]), int(time[4:]))
#         alls[d] = ask


# sortedKeys = sorted(alls.keys())
# print sortedlsKeys[:10]


# In[193]:

trainer = BackpropTrainer(n, ds)


# In[195]:

# trainer.trainUntilConvergence()
# trainer.train()

import pickle

# In[168]:

for x in range(10000):
    if x % 50 == 0:
        print "Error on iteration " + str(x) + ": " + str(trainer.train())
        pickle.dump(n, open('network.pkl', 'wb'))

    trainer.train()

print n
# # In[196]:

# directions = []
# errors = []
# for d in test:

#     out = n.activate(d[0])
#     errors.append(out**2)
#     out = out
# #     print out, d[1]
#     directions.append((out[0] < 0 and d[1] < 0) or (out[0] > 0 and d[1]  > 0)) #30 min pre


# # In[197]:

# print "SSE: " + str(sum(errors))
# print "Pct in correct direction: " + str(directions.count(True)/float(len(directions)))


# # In[198]:

# cache = {}
# count = 0
# for k in sortedKeys:
#     cache[k] = count
#     count += 1


# def moving_average(delta, data, date):
# #     date = date - delta
#     kys = sortedKeys
# #     print kys
#     i1, i2 = 1, 1
# #     print delta.hours
#     try:
#         d1 = closest_date(date)
#         i1 = cache[d1]
#     except:
#         count = 0
#         for k in kys:
#     #       print k
#             if k > date:
#                 i1 = count
#                 break   
#         count += 1
#     try:
#         d2 = closest_date(date - delta)
#         i2 = cache[d2]
#     except:
#         count = 0
#         for k in kys:
#     #       print k
#             if k > date - delta:
#                 i2 = count
#                 break   
#             count += 1#     print d1, d2
#     points = []

#     #compute avg approx for speed
#     datapoints = 5
#     ptz = []
#     if abs(i1-i2)/5 == 0:
#         return mean([float(alls[kys[i1]]), float(alls[kys[i2]])])
#     for z in range(i1, i2, abs(i1-i2)/5):
#         ptz.append(float(alls[kys[z]]))
#     return mean(ptz)
#     for z in kys[i2:i1]:
#         if z < date:
#             points.append(float(alls[z]))
#     return mean(points)
# tree = lambda: defaultdict(tree)
# dct = tree()

# def get_past_averages(date, dct=dct):
# #     print date
#     vec = []
#     for back in [1/24.0,.25,1,3,7,31,90,180,365]:

# #         if back < 1:    
# #             dlt = datetime.timedelta(hours=back*24)

# #             vec.append(moving_average_hours(dlt, dct, date))
# #         else:
#         dlt = datetime.timedelta(days=back)

#         vec.append(moving_average(dlt, dct, date))
#     return vec

# def closest_datapoint(d):
#     closest =  dct[d.year][d.month][d.day][d.hour][d.minute]
#     if str(type(closest)) != "<type 'collections.defaultdict'>":
#         return closest
#     else:
#         return closest_datapoint(d + datetime.timedelta(seconds=60))

# def closest_date(d):
#     closest =  dct[d.year][d.month][d.day][d.hour][d.minute]
#     if str(type(closest)) != "<type 'collections.defaultdict'>":
#         return datetime.datetime(d.year,d.month,d.day,d.hour,d.minute)
#     else:
#         return closest_date(d + datetime.timedelta(seconds=120))


# # d = datetime.datetime(2015,2,4,1,1)

# # print get_past_averages(d)




