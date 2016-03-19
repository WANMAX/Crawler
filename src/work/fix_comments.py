'''
Created on 2016年1月16日

@author: wan
'''
import __init__
from store.database_args import get_conn
from store.news.file_ import STORE_DIR, _CHARSET
from store.news.database import NEWS_DIT
import os
import re
import importlib
from web.news import _NEWS_MODULE_PATH
from store.news import database
from threading import Thread
from util import thread_pool


NEWS_ID_SQL = "select news_id from news where news_website_id = %u and news_title = '%s'"
def get_news_id(module_str, title, cur):
    sql = NEWS_ID_SQL%(NEWS_DIT[module_str], title)
    cur.execute(sql)
    return cur.fetchone()[0]
count = 0
def do_item(path, module_str, title):
    conn = get_conn()
    cur = conn.cursor()
    news_id = get_news_id(module_str, title, cur)
    sql = 'select count(*) from news_comment where news_id = %u'%news_id
    cur.execute(sql)
    if cur.fetchone()[0]:
        cur.close()
        conn.close()
        return
    else:
        global count
        count += 1
        print(id, count)
    module = importlib.import_module(_NEWS_MODULE_PATH%module_str)
    with open(path, 'r', encoding=_CHARSET, errors='ignore') as file:
        lines = ''
        for line in file:
            lines += line
            try:
                comment = module.match_comment(eval(lines))
                database.store_comment(comment, news_id, cur)
            except:
                pass
            else:
                lines = ''
    cur.close()
    conn.commit()
    conn.close()

DIR = STORE_DIR%'%s2/comments_source_code'
def do(module_str='wangyi'):
    path = DIR%module_str
    for item in os.listdir(path):
        title = item.replace('.txt', '')
        title = re.sub('(_新闻)_腾讯网', '', title)
        yield Thread(target=do_item, args=(path+item, module_str, title))

if __name__ == '__main__':
    list_ = ['tencent', 'sohu']
    for item in list_:
        thread_pool.set_generator(do(item))
        thread_pool.start()
        thread_pool.join()
