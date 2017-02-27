#!/usr/bin/python3
__author__ = "Pushkar Gujar"

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import csv
from datetime import datetime
import os

url = 'https://www.verizonwireless.com/smartphones/samsung-galaxy-s7/'

browser = webdriver.Chrome(executable_path='/Users/pushkargujar/PycharmProjects/Verizon/chromedriver')
browser.get(url)
reviews = []
dates = []
review_section = '//*[@id="BVRRContainer"]/div/div/div/div/ol/li[*]/div/div[1]' \
                 '/div/div[2]/div/div/div[1]/p'
date_section = '//*[@id="BVRRContainer"]/div/div/div/div/ol/li[*]/div/div[1]' \
               '/div/div[1]/div/div[1]/div/div/div/div/meta[2]'

try:
    numReviews = int((browser.find_element_by_xpath(
        '//*[@id="BVRRSearchContainer"]/div/div/div/div/div/div[1]/div/dl/dd[3]/span/a') \
                      .text
                      ).split(" ")[0]
                     )
except:
    numReviews = 4000

print("Found {} reviews".format(numReviews))

# read first ten pages of reviews ==>
while True:

    for review in browser.find_elements_by_xpath(review_section):
        reviews.append(review.text)
    for pub_date in browser.find_elements_by_xpath(date_section):
        dates.append(pub_date.get_attribute('content'))

    try:
        next = browser.find_element_by_xpath('//*[@id="BVRRContainer"]/div/div/div/div/div[3]/div/ul/li[2]/a/span[2]')
        next.location_once_scrolled_into_view
        time.sleep(0.5)  # To wait until scrolled down to "Next" button
        next.click()
        time.sleep(2)  # To wait for page "autoscrolling" to first review + until modal window dissapeared
    except WebDriverException:
        pass

    if len(reviews) >= min(numReviews, 4000):  # exit when at least 4000 reviews found
        break

# filename = output_year-month-date-hour.csv
filename = "scrapped_" + str(datetime.today())[:13].replace(" ", "-") + ".csv"

output_path = os.environ['HOME']+"/data/"\
                + str(datetime.today().year)+"/"\
                + str(datetime.today().month)+"/"\
                + str(datetime.today().day)+"/"\
                + str(datetime.today().hour)

if not os.path.exists(output_path):
    os.makedirs(output_path)

# write output to csv file
with open(output_path+"/"+filename, "w+") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(zip(dates, reviews))

browser.quit()


