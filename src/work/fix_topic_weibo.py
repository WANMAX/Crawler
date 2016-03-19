'''
Created on 2016年1月28日

@author: wan
'''
import __init__
from store.database_args import get_conn
from store.weibo.database import match_topic
from web.weibo.sina import content, login_all_default_user
from store.weibo import database

def todo(source_list, store_args):
    result = [content.match_item(source_code) for source_code in source_list[:5]]
    database.store_weibos(result, store_args)
sql_pat = 'select * from weibo_hotspot'
sql_pat2 = 'select * from weibo_hotspot_relative where weibo_hotspot_id = %u'
def get_topic_list():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql_pat)
    for item in cur.fetchall():
        sql = sql_pat2%item[0]
        if not cur.execute(sql):
            yield item
    cur.close()
    conn.close()
def work():
    login_all_default_user()
    for topic in get_topic_list():
        topic = match_topic(topic)
        print(topic.topic_name)
        store_args = ('sina', topic.topic_name)
        page_id, domain = topic.topic_args
        try:
            content.crawl(page_id, domain, todo, store_args, 1)
        except:
            pass

if __name__ == '__main__':
    work()
