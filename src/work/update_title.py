'''
Created on 2016年1月15日

@author: wan
'''
import __init__
from store.database_args import get_conn
import re
from util.urlopen_and_read import urlopen_and_read
from bs4 import BeautifulSoup as Soup
from web.news.tencent import NEWS_CHARSET 
from work.single_news_work import NAME_PAT
from store.news import file_
from util import thread_pool

DIR = file_.STORE_DIR
DIR = DIR%'tencent/国内'
FILE = DIR + '%s'


SQL_PAT = "update news set news_title = '%s' where news_id = %u"
def do_item(item):
    conn = get_conn()
    cur = conn.cursor()
    title = Soup(urlopen_and_read(item[2]).decode(NEWS_CHARSET, 'ignore')).title.text
    title = re.sub('(_新闻)_腾讯网', '', title)
    title = re.sub(NAME_PAT, '', title)
    sql = SQL_PAT%(title, item[0])
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print(title)
    
def do(): 
    conn = get_conn()
    cur = conn.cursor()
    sql = 'select news_id, news_title, news_url from news'
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        sql = 'delete from news_comment where news_id = %u'%item[0]
        cur.execute(sql)
        conn.commit()
        if re.search('^\\S$', item[1]):
            thread_pool.add(do_item, (item,))
    thread_pool.start()
    thread_pool.join()
    cur.close()
    conn.close()
if __name__ == '__main__':
    do()
