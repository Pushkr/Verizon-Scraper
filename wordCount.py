#!/usr/bin/python3
__author__ = "Pushkar Gujar"

from pyspark import SparkContext, SparkConf
from datetime import datetime

conf = SparkConf().setAppName("Verizon_1.0: Reviews Data Analysis")
sc = SparkContext(conf=conf)

# reconstruct hourly file name
filename_suffix = str(datetime.today())[:13].replace(" ", "-")
infile = "scraped_" + filename_suffix
# infile = "scraped_2017-02-23-17-17.csv"

try:
    file = sc.textFile("hdfs://localhost:9000/user/pushkargujar/verizon/indata/" + infile).cache()
    file.take(1)  # to test if file exists
    file_Available = "Yes"
except:
    file_Available = "No"
    print("File Not Available {}".format("hdfs://localhost:9000/user/pushkargujar/verizon/indata/" + infile))

if file_Available == "Yes":

    wordList = file.map(lambda row: row.split(",")[1]) \
        .flatMap(lambda row: row.split(" ")).map(lambda word: (word, 1)) \
        .reduceByKey(lambda x, y: x + y) \
        .sortBy(lambda row: row[1], ascending=False) \
        .map(lambda row: row[0] + "," + str(row[1])) \
        .take(250)

    sc.parallelize(wordList). \
        saveAsTextFile("hdfs://localhost:9000/user/pushkargujar/verizon/outdata/parsed_" + filename_suffix)
else:
    sc.stop()
