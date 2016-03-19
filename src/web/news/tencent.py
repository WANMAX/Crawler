'''
Created on 2015年11月9日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
import re
import time

from util.class_ import News, Comment
from util.dict_extra import true, false
from web.news import BY_LAST_ID
import util.get_news_url_list_from_baidu_templet


NEWS_CHARSET = COMMENT_CHARSET = 'gb2312'
TYPE=BY_LAST_ID

get_news_url_list = util.get_news_url_list_from_baidu_templet.get_mothed('news.qq.com', 'http://news.qq.com/a/.+')
def match_news(html, url):
    cmt_id = re.search('cmt_id[\\s\\S]+?(\\d+)', html)
    if not cmt_id:return
    cmt_id = cmt_id.group(1)
    comment_url_args = (cmt_id,)
    soup = Soup(html)
    title = soup.title.text
    try:
        div = soup.find('div', {'bosszone':'content'})
        if div.img:
            news_image = div.img['src']
        else:
            news_image = None
        content = '\n'.join([temp.strip() for temp in [item.get_text() for item in div.find_all('p')] if not re.match('\\s*$', temp)])
    except:
        content = ''
        news_image = None
    source_span = soup.find('span', {'bosszone':'jgname'})
    source = source_span.get_text()
    try:
        source_url = source_span.a['href']
    except:
        source_url = None
    date = soup.find('span', {'class':'article-time'}).get_text()
    date = time.strptime(date,"%Y-%m-%d %H:%M")
    date = time.mktime(date)
    return News(url, comment_url_args, title, content, source, date, source_url, news_image=news_image)
def get_type(html):
    sub_name = re.search("subName:{[\\s\\S]+?}", html).group()
    return re.search("cname:'([\\s\\S]+?)'", sub_name).group(1)
def get_comment_page_url(id_, args):
    url = 'http://coral.qq.com/article/%s/comment' % args[0]
    if not id_:
        return url
    return url + '?commentid=%s'%id_
def has_next(html):
    return eval(html)['data']['hasnext']
def get_next_id(html):
    return eval(html)['data']['last']
def get_comment_source_list(html):
    return eval(html)['data']['commentid']
def match_comment(comment_source_code):
    userid = 'tx%s'%comment_source_code['userid']
    content = comment_source_code['content'].strip()
    time_ = comment_source_code['time']
    vote = eval(comment_source_code['up'])
    return Comment(userid, content, time_, vote=vote)
