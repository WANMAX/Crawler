'''
Created on 2015年11月13日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
import re
from util.class_ import WEIBO_COMMENT as Comment
import time
from util.dict_extra import null
from web.weibo.sina import change_user, test_cookie, get_current_user, delete_cookie, urlopen, ignore_emoji, INTERVAL

_CHARSET = 'utf-8'

def _crawl_page(mid, page):
    try_ = 3
    while get_current_user():
        try:
            url = 'http://weibo.com/aj/v6/comment/big?id=%s'%mid
            if page != 1:
                url += '&page=%u' % page
            html = urlopen(url).read().decode(_CHARSET)
            change_user()
            time.sleep(INTERVAL)
            try_ = 3
            return ignore_emoji(html)
        except:
            current_user = get_current_user()
            tag = test_cookie(current_user)
            if tag:
                if not try_:raise
                try_ -= 1
            change_user()
            if not tag:
                delete_cookie(current_user)
def _date_format(date):
    if '-' in date:
        format_ = '%Y-%m-%d %H:%M'
        date = time.strptime(date, format_)
        date = time.mktime(date)
    elif '月' in date:
        format_ = '%m月%d日 %H:%M'
        date = time.strptime(date, format_)
        date = list(date)
        date[0] = time.localtime(time.time())[0]
        date = time.mktime(tuple(date))
    elif '今天' in date:
        format_ = '今天 %H:%M'
        date = time.strptime(date, format_)
        date = list(date)
        date[:3] = time.localtime(time.time())[:3]
        date = time.mktime(tuple(date))
    else:
        negative_minute = int(re.search('\\d+', date).group())
        date = list(time.localtime(time.time()))
        if date[4] >= negative_minute:
            date[4] -= negative_minute
        else:
            date[3] -= 1
            date[4] = date[4] + 60 - negative_minute
        date = time.mktime(tuple(date))
    return date
def match_item(soup):
    comment_id = soup['comment_id']
    uid = re.search('id=(\\d+)', soup.find('a', {'usercard':True})['usercard']).group(1)
    content = re.sub('^[^：]+：', '', soup.find('div', 'WB_text').get_text().strip())
    date = soup.find('div', re.compile('S_txt2')).get_text().strip()
    date = _date_format(date)
    return Comment(comment_id, uid, content, date)
def _get_comments_soup(html):
    LIST = []
    soup = Soup(html)
    for temp in soup.find_all('div', {'comment_id':True}):
        LIST.append(temp)
    return LIST
def crawl(mid, todo, store_args, counter=None):
    page = 1
    data = eval(_crawl_page(mid, page))['data']
    if data['count'] == 0:
        return
    pages = data['page']['totalpage']
    html = data['html'].replace(r'\/', '/')
    comment_source_list = _get_comments_soup(html)
    if comment_source_list:
        todo(comment_source_list, store_args)
    if counter:
        counter.count()
    while page < pages:
        page += 1
        html = eval(_crawl_page(mid, page))['data']['html'].replace(r'\/', '/')
        comment_source_list = _get_comments_soup(html)
        if comment_source_list:
            todo(comment_source_list, store_args)
        if counter:
            counter.count()
