# -*- encoding: utf-8 -*-

import tweepy
from tweepy.parsers import JSONParser
from datetime import date, timedelta
import time

API_KEY = ''
API_SECRET = ''
ACCESS_KEY = '-'
ACCESS_SECRET = ''

oAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oAuth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth_handler = oAuth, api_root = '/1.1', parser=JSONParser())

if __name__ == "__main__":
    # TOPIC SELECTION & FILE OPEN
    topic = '사랑 그리움'
    f = open(topic+'.txt', 'a')
    # DATE SUBTRACTION
    delta = 0
    delay_flag = False

    for j in range(100):
        delta = j
        date = date.today() - timedelta(days=delta)
        print('loop in times:', '%s' % j, str(date))
        if delay_flag == True:
            time.sleep(3600)
            delta = 0
            date = date.today() - timedelta(days=delta)
            try:
                result = api.search(q=topic, count=100, until=date)
                for i in range(100):
                    f.write(result['statuses'][i]['text'])
            except:
                pass
        # SEARCH REQUEST
        result = api.search(q=topic, count=100, until=date)
        for i in range(100):
            if i is 0:
                try:
                    print(result['statuses'][i]['text'])
                except:
                    print('결과가 검색되지 않았습니다.')
                    delay_flag = True
            try:
                f.write(result['statuses'][i]['text'])
                #print(result['statuses'][i]['retweet_count'])
            except:
                pass
        time.sleep(5)
    f.close()