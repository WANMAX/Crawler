'''
Created on 2015年11月9日

@author: wan
'''
import __init__
import datetime
import time
from threading import Thread
import work.single_news_work
import logging
from __init__ import WORK_PATH

NEWS_LIST = ['tencent', 'sohu', 'sina', 'ifeng', 'wangyi']
START_FROM_THIS_TIME_NEWS_LIST = []
STORE_TYPE = 'database'

WEIBO_WORKING = False

def _work_news():
    for news in NEWS_LIST:
        if news in START_FROM_THIS_TIME_NEWS_LIST:
            work.single_news_work.work(news, STORE_TYPE)
        else:
            START_FROM_THIS_TIME_NEWS_LIST.append(news)
def main():
    start_time = datetime.date.min
    while True:
        now = datetime.datetime.today()
        hour = now.hour
        now = datetime.date(now.year, now.month, now.day)
        if now>start_time and hour>=12:
            start_time = now
            Thread(target=_work_news).start()
        time.sleep(1)

if __name__ == '__main__':
    logging.config.fileConfig('%s/logging_config.conf'%WORK_PATH)
    main()
