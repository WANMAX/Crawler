'''
Created on 2016年1月18日

@author: wan
'''
import os
from store.database_args import get_conn
import datetime
import time


STORE_DIR = os.path.dirname(os.path.realpath(__file__))
STORE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(STORE_DIR)))
MIDS_PATH = '%s/weibo/'%STORE_DIR+'%s/temp/%s/weibo.txt'
FILE_CHARSET = 'utf-8'


HOTSPOT_ID_SQL_PAT = "select weibo_hotspot_id from weibo_hotspot where weibo_hotspot_name = '%s'"
def get_result_mids(store_args):
    conn = get_conn()
    cur = conn.cursor()
    sql = HOTSPOT_ID_SQL_PAT%store_args[1]
    cur.execute(sql)
    topic_id = cur.fetchone()[0]
    sql = "select weibo_id from weibo_hotspot_relative where weibo_hotspot_id = %u"%topic_id
    cur.execute(sql)
    for mid in cur.fetchall():
        yield mid[0]
    cur.close()
    conn.close()
get_mids = get_result_mids
sql_pat = 'select * from weibo where weibo_id = %s'
sql_pat1 = "update weibo where weibo_id = %s"
sql_pat2 = "insert into weibo (weibo_id, weibo_content, weibo_userid, weibo_datetime) values (%s, '%s', '%s', '%s')"
sql_pat3 = "insert into weibo_hotspot_relative (weibo_id, weibo_hotspot_id) values (%s, %s)"
def _store_weibo(weibo, topic_id, cur):
    sql = sql_pat%weibo.mid
    if cur.execute(sql):
        return
    else:
        sql = sql_pat2%(weibo.mid, weibo.content.replace("'", "\\'"), weibo.uid, datetime.datetime(*time.localtime(weibo.time)[:6]))
        cur.execute(sql)
        sql = sql_pat3%(weibo.mid, topic_id)
        cur.execute(sql)
def store_weibos(weibos, store_args):
    if not weibos:
        return
    conn = get_conn()
    cur = conn.cursor()
    sql = HOTSPOT_ID_SQL_PAT%store_args[1]
    cur.execute(sql)
    topic_id = cur.fetchone()[0]
    for weibo in weibos:
        _store_weibo(weibo, topic_id, cur)
    conn.commit()
    cur.close()
    conn.close()
sql_pat4 = 'select * from weibo_comment where weibo_comment_id = %s'
sql_pat5 = "insert into weibo_comment (weibo_comment_id, weibo_comment_content, weibo_comment_userid, weibo_comment_datetime) values (%s, '%s', '%s', '%s')"
sql_pat6 = "insert into weibo_comment_relative (weibo_id, weibo_comment_id) values (%s, %s)"
def _store_comment(comment, store_args, cur):
    sql = sql_pat4%comment.id
    if cur.execute(sql):
        return
    else:
        sql = sql_pat5%(comment.id, comment.content.replace("'", "\\'"), comment.user_id, datetime.datetime(*time.localtime(comment.time)[:6]))
        cur.execute(sql)
        sql = sql_pat6%(store_args[2], comment.id)
        cur.execute(sql)
def store_comments(comments, store_args):
    if not comments:
        return
    conn = get_conn()
    cur = conn.cursor()
    for comment in comments:
        _store_comment(comment, store_args, cur)
    conn.commit()
    cur.close()
    conn.close()
sql_pat7 = 'select * from weibo_repost where weibo_repost_id = %s'
sql_pat8 = "insert into weibo_repost (weibo_repost_id, weibo_repost_content, weibo_repost_userid, weibo_repost_datetime) values (%s, '%s', '%s', '%s')"
sql_pat9 = "insert into weibo_repost_relative (weibo_id, weibo_repost_id) values (%s, %s)"
def _store_repost(repost, store_args, cur):
    sql = sql_pat7%repost.id
    if cur.execute(sql):
        return
    else:
        sql = sql_pat8%(repost.id, repost.content.replace("'", "\\'"), repost.user_id, datetime.datetime(*time.localtime(repost.time)[:6]))
        cur.execute(sql)
        sql = sql_pat9%(store_args[2], repost.id)
        cur.execute(sql)
def store_reposts(reposts, store_args):
    if not reposts:
        return
    conn = get_conn()
    cur = conn.cursor()
    for repost in reposts:
        _store_repost(repost, store_args, cur)
    conn.commit()
    cur.close()
    conn.close()
def end(store_args):
    pass
sql_pat10 = "select * from weibo_hotspot where weibo_hotspot_name = '%s'"
sql_pat11 = "insert into weibo_hotspot (weibo_hotspot_name, weibo_hotspot_datetime, weibo_hotspot_type, weibo_hotspot_introduction, weibo_hotspot_args) \
values ('%s', '%s', '%s', '%s', '%s')"
def test_topic(topic_name,  weibo_module_str):
    conn = get_conn()
    cur = conn.cursor()
    sql = sql_pat10%topic_name
    if cur.execute(sql):return False
    else:return True
    cur.close()
    conn.close()
def store_topics(topics, store_args):
    if not topics:return
    conn = get_conn()
    cur = conn.cursor()
    for topic in topics:
        sql = sql_pat11%(topic.topic_name, datetime.datetime(*time.localtime(topic.topic_datetime)[:6]),
                         topic.topic_type, topic.topic_introduction.replace("'", "\\'"), str(topic.topic_args).replace("'", "\\'"))
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
sql_pat12='select weibo_hotspot_id from event_weibo_relative where active_not = 1'
sql_pat13='select * from weibo_hotspot where weibo_hotspot_id = %u'
from util.class_ import Topic
def match_topic(item):
    return Topic(item[1], time.mktime(item[2].timetuple()), item[3], item[4], eval(item[5]))
def get_topics(weibo_module_str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql_pat12)
    for item in cur.fetchall():
        sql = sql_pat13%item[0]
        cur.execute(sql)
        item = cur.fetchone()
        yield match_topic(item)
    cur.close()
    conn.close()
if __name__ == '__main__':
    for item in  get_topics('sina'):
        print(item)