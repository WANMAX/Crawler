'''
Created on 2015年11月17日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
import re
from util.class_ import Repost
from util.dict_extra import null
from web.weibo.sina import change_user, test_cookie, get_current_user, delete_cookie, urlopen, ignore_emoji, INTERVAL
import time

_CHARSET = 'utf-8'

def _crawl_page(mid, page):
    try_ = 3
    while get_current_user():
        try:
            url = 'http://weibo.com/aj/v6/mblog/info/big?id=%s'%mid
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
def match_item(soup):
    repost_id = soup['mid']
    uid = re.search('id=(\\d+)', soup.find('a', {'usercard':True})['usercard']).group(1)
    content = soup.find('span', {'node-type':'text'}).get_text().strip()
    date = eval(soup.find('a', {'node-type':'feed_list_item_date'})['date'])/1000
    return Repost(repost_id, uid, content, date)
def _get_reposts_soup(html):
    LIST = []
    soup = Soup(html)
    for temp in soup.find_all('div', {'action-type':'feed_list_item'}):
        LIST.append(temp)
    return LIST
def crawl(mid, todo, store_args, counter=None):
    page = 1
    data = eval(_crawl_page(mid, page))['data']
    if data['count'] == 0:
        return
    pages = data['page']['totalpage']
    html = data['html'].replace(r'\/', '/')
    repost_source_list = _get_reposts_soup(html)
    if repost_source_list:
        todo(repost_source_list, store_args)
    if counter:
        counter.count()
    while page < pages:
        page += 1
        html = eval(_crawl_page(mid, page))['data']['html'].replace(r'\/', '/')
        repost_source_list = _get_reposts_soup(html)
        if repost_source_list:
            todo(repost_source_list, store_args)
        if counter:
            counter.count()
