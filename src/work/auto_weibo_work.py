'''
Created on 2016年1月28日

@author: wan
'''
import __init__
import datetime
import logging.config
import time
from threading import Thread
from work import weibo_topic, single_weibo_work
from util.counter import Counter
weibo_module_str = 'sina'
store_module_str = 'database'
start_at_this_time = [False, False]

IS_ALIVE = False
def weibo_topic_work():
    global IS_ALIVE
    IS_ALIVE = True
    weibo_topic.work(weibo_module_str, store_module_str)
    IS_ALIVE = False
def weibo_work():
    global IS_ALIVE
    IS_ALIVE = True
    counter = Counter(logging.getLogger('crawlerLog'), 10, 20)
    single_weibo_work.work(weibo_module_str, store_module_str, counter)
    IS_ALIVE = False
def main():
    global start_at_this_time
    start_time = datetime.date.min
    start_time2 = datetime.date.min
    while True:
        now = datetime.datetime.today()
        hour = now.hour
        now = datetime.date(now.year, now.month, now.day)
        if now>start_time and hour>=0:
            start_time = now
            if not start_at_this_time[0]:start_at_this_time[0] = True
            elif not IS_ALIVE:
                Thread(target=weibo_topic_work).start()
        time.sleep(1)
        if now>start_time2 and hour>=6:
            start_time2 = now
            if not start_at_this_time[1]:start_at_this_time[1] = True
            elif not IS_ALIVE:
                Thread(target=weibo_work).start()
        time.sleep(1)
    
if __name__ == '__main__':
    logging.config.fileConfig('../logging_config.conf')
    main()