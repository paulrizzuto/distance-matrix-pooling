#!/usr/bin/env python
from multiprocessing.pool import ThreadPool
from time import time as timer
from urllib.request import urlopen
import requests
import json
import csv
import os

csvpath = os.path.join('citystate1.csv')

gkey = GOOGLE_KEY

urls = []

#for loop for creating url list, counter for when to start pooling
counter = 0
with open(csvpath, newline= "") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    next(csvreader)

    for row in csvreader:
        city = row[0]
        state = row[1]
        city2 = row[2]
        state2 = row[3]
        origin_city = city + "," + state
        destination_city = city2 + "," + state2
        urls.append("https://maps.googleapis.com/maps/api/distancematrix/json" \
        "?origins=%s&destinations=%s&units=imperial&key=%s" % (origin_city, destination_city, gkey))
        counter = counter + 1

#make api requests
def dist_matrix(url):
    try:
        response = requests.get(url).json()
        return url, response["rows"][0]["elements"][0]["duration"]["text"]
    except Exception as e:
        return url, None, e

#if url list is built, start pooling and calling function
if counter >= 950:
    start = timer()
    print("Timer started")
    results = ThreadPool(20).imap_unordered(dist_matrix, urls)
    for url, time in enumerate(results):
        print(url, time)
    print("Elapsed Time: %s" % (timer() - start,))

else:
    print(counter)
