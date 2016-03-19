'''
Created on 2016年1月14日

@author: wan
'''

import time
import datetime
from store.database_args import get_conn




conn = None

NEWS_DIT = {'tencent':1, 'wangyi':2, 'sohu':3, 'sina':4, 'ifeng':5}
NEWS_PAT = \
'''insert into news (news_website_id, news_website_type, news_url, news_comment_url_args, news_title, news_abstract,
news_content, news_source, news_source_url, news_author, news_datetime, news_image)
values (%u, '%s', '%s', '%s', '%s', %s, '%s', '%s', %s, %s, '%s', %s)'''

def store_news(news, store_args):
    conn = get_conn()
    cur = conn.cursor()
    sql = "select * from news where news_website_id = %u and news_title = '%s'"%(NEWS_DIT[store_args[0]], store_args[1])
    if cur.execute(sql):return
    if news.abstract:
        abstract = "'%s'"%news.abstract
    else:
        abstract = 'Null'
    if news.source_url:
        source_url = "'%s'"%news.source_url
    else:
        source_url = 'Null'
    if news.author:
        author = "'%s'"%news.author
    else:
        author = 'Null'
    if news.news_image:
        news_image = "'%s'"%news.news_image
    else:
        news_image = 'Null'
    sql = NEWS_PAT%(NEWS_DIT[store_args[0]], store_args[1], news.url, str(news.comment_url_args).replace("'", "\\'"), store_args[2], abstract,
                        news.content.replace("'", "\\'"), news.source, source_url, author, datetime.datetime(*time.localtime(news.date)[:6]), news_image)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

COMMENT_PAT = \
'''insert into news_comment (news_id, news_comment_userid, news_comment_content, news_comment_datetime,
news_comment_user_place, news_comment_goodnumber)
values (%u, '%s', '%s', '%s', %s, %u)'''
def _store_comment(comment, news_id, cur):
    if comment.location:
        location = "'%s"%comment.location
    else:
        location = 'Null'
    if comment.vote:
        try:
            vote = eval(comment.vote)
        except:
            vote = 0
    else:
        vote = 0
    sql = COMMENT_PAT%(news_id, comment.user_id, comment.content.replace("'", "\\'"), datetime.datetime(*time.localtime(comment.time)[:6]),
                        location, vote)
    try:
        cur.execute(sql)
    except:
        pass
NEWS_ID_SQL = "select news_id from news where news_website_id = %u and news_website_type = '%s' and news_title = '%s'"
def store_comments(comments, store_args):
    conn = get_conn()
    cur = conn.cursor()
    sql = NEWS_ID_SQL%(NEWS_DIT[store_args[0]], store_args[1], store_args[2])
    cur.execute(sql)
    news_id = cur.fetchone()
    if not news_id:
        return
    for comment in comments:
        _store_comment(comment, news_id[0], cur)
    conn.commit()
    cur.close()
    conn.close()
