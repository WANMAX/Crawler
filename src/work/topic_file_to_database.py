'''
Created on 2016年1月15日

@author: wan
'''
import __init__
from store.weibo.database import sql_pat11
from store.weibo.file_ import match_topic
from work import WORK_PATH
from util import thread_pool
from threading import Thread
from store.database_args import get_conn
import datetime
import time

def do_item(topic):
    conn = get_conn()
    cur = conn.cursor()
    sql = sql_pat11%(topic.topic_name, datetime.datetime(*time.localtime(topic.topic_datetime)[:6]),
                     topic.topic_type, topic.topic_introduction.replace("'", "\\'"), str(topic.topic_args).replace("'", "\\'"))
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
path = WORK_PATH + '/work/temp'
def _get_list_item():
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            yield Thread(target=do_item, args=(match_topic(line),))
def do():
    thread_pool.set_generator(_get_list_item())
    thread_pool.start()
    thread_pool.join()

if __name__ == '__main__':
    do()
