#!/usr/bin/python3
from random import *
import pandas as pd
import string
import pymysql
import time
from datetime import datetime

# util class for generating random date and random text
class Generator:
    @staticmethod
    def random_datetime():
        MM = randint(1, 12)
        DD = randint(1, 28)
        hh = randint(0, 23)
        mm = randint(0, 59)
        ss = randint(0, 59)
        return datetime(2017, MM, DD, hh, mm, ss).isoformat(' ')

    @staticmethod
    def random_text(size):
        return ''.join(choice(string.ascii_lowercase + string.ascii_lowercase
                                     + string.digits + ' ' * 20 + '#' * 2) for _ in range(size))

# make a list of user ids
userIDs = sample(range(1000000, 10000000), 10000)
tweetIDs = sample(range(10000000, 100000000), 1000000)
userIDCol = []
dateCol = []
textCol = []
# create the tweets and stored in a dataframe before inserting
for i in userIDs:
    for x in range(0, 100):
        userIDCol.append(i)
        dateCol.append(Generator.random_datetime())
        textCol.append(Generator.random_text(randint(10, 100)))
dic = {"tweetID": tweetIDs, "userID": userIDCol, "dateTime": dateCol, "text": textCol}
tweets = pd.DataFrame(dic)

# Open database connection
db = pymysql.connect("localhost", "root", "j19y96t00", "Twitter")
cursor = db.cursor()

# create followers, assuming 80 followers per user
for i in userIDs:
    following = sample([x for x in userIDs if x != i], 80)
    for y in following:
        sql = "INSERT INTO FOLLOWERS(user_id, follows_id) VALUES ('%d', '%d')" % \
          (i, y)
        cursor.execute(sql)

# insert generated tweets
start = time.time()
for row in tweets.itertuples():
    sql = "INSERT INTO TWEETS(tweet_id, user_id, tweet_text) VALUES ('%d', '%d', '%s')" % \
          (row[3], row[4], row[2])
    cursor.execute(sql)

end = time.time()
print(end - start)
mostRecentTweets = []

# clsoe connection
db.close()