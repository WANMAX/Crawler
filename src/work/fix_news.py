'''
Created on 2016年1月19日

@author: wan
'''

import __init__
from store.database_args import get_conn
from util import  thread_pool
from threading import Thread
import os
STORE_DIR = os.path.dirname(os.path.realpath(__file__))
STORE_PATH = '%s/temp'%STORE_DIR
with open(STORE_PATH, 'r', encoding='utf-8', errors='ignore') as file:
    count = 0
    for line in file:
        count += 1
        if count == 1:
            CHANGE_LIST = eval(line)
        elif count == 2:
            CHANGE_LIST2 = eval(line)

sql_pat = "select news_id from news where news_url like '%s%%'"
def _do_item(item):
    conn = get_conn()
    cur = conn.cursor()
    news_id, news_url = item
    if '?' in news_url:
        news_url = news_url[:news_url.find('?')]
    sql = sql_pat%news_url
    if cur.execute(sql) == 1:
        cur.close()
        conn.close()
        return
    cl = [item[0] for item in cur.fetchall()]
    global CHANGE_LIST
    if news_id not in CHANGE_LIST:
        CHANGE_LIST.append(news_id)
        print(news_id)
    for news_id in cl:
        if news_id not in CHANGE_LIST:
            CHANGE_LIST.append(news_id)
            print(news_id)
    cur.close()
    conn.close()
count = 1
def get_NEWS_ID_LIST():
    conn = get_conn()
    cur = conn.cursor()
    sql = 'select news_id, news_url from news'
    cur.execute(sql)
    for item in cur.fetchall():
        if item in CHANGE_LIST:
            continue
        yield Thread(target=_do_item, args=(item,))
        global count
        print(count)
        if CHANGE_LIST:
            print(CHANGE_LIST)
        count += 1
    cur.close()
    conn.close()
def do_with_news():
    conn = get_conn()
    cur = conn.cursor()
    for item in CHANGE_LIST:
        sql = 'select news_url from news where news_id = %u'%item
        if not cur.execute(sql):continue
        news_id = cur.fetchone()[0]
        sql = sql_pat%news_id
        cur.execute(sql)
        if cur.fetchone()[0] == 1:
            continue
        try:
            sql = 'delete from news where news_id = %u'%item
            cur.execute(sql)
            conn.commit()
        except:
            pass
    cur.close()
    conn.close()
def do_with_comment(item):
    conn = get_conn()
    cur = conn.cursor()
    sql = 'select * from news_comment where news_id = %u order by news_comment_datetime'%item
    if not cur.execute(sql):return
    temp = ()
    for item in cur.fetchall():
        if temp[1:] == item[1:]:
            sql = 'delete from news_comment where news_comment_id = %u'%temp[0]
            cur.execute(sql)
            conn.commit()
        temp = item
    cur.close()
    conn.close()
def do_with_comments():
    global count
    for item in CHANGE_LIST2:
        thread = Thread(target=do_with_comment, args=(item,))
        print(item, thread)
        yield thread
        print(count)
        count += 1
        
def do():
    thread_pool.set_generator(do_with_comments())
    thread_pool.start()
    thread_pool.join()
do_with_comment(29999)
