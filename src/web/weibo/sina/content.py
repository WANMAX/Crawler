'''
Created on 2015年11月16日

@author: wan
'''
import re
from bs4 import BeautifulSoup as Soup
from util.class_ import Weibo
import time
from web.weibo.sina import change_user, test_cookie, get_current_user,\
    delete_cookie, urlopen, ignore_emoji, INTERVAL

_CHARSET = 'utf-8'
DEBUG = False


def _crawl_page(page_id, domain, page):
    try_ = 3
    while get_current_user():
        try:
            url = 'http://weibo.com/p/%s?page=%u' %(page_id,  page)
            url2 = 'http://weibo.com/p/aj/v6/mblog/mbloglist?domain=%s&page=%u&pre_page=%u&pagebar=0&pl_name=Pl_Third_App__9&id=%s&feed_type=1'%(domain, page, page, page_id)
            url3 = 'http://weibo.com/p/aj/v6/mblog/mbloglist?domain=%s&page=%u&pre_page=%u&pagebar=1&pl_name=Pl_Third_App__9&id=%s&feed_type=1'%(domain, page, page, page_id)
            html = urlopen(url).read().decode(_CHARSET, errors='ignore')
            if page==1:
                for temp in Soup(html).find_all('script', text=re.compile('{"ns":"pl\.content\.homeFeed\.index"')):
                    temp = temp.get_text()
                    if temp.find('主持人推荐')==-1 and temp.find('热门讨论')!=-1:
                        html = temp
                        break
            else:
                html = Soup(html).find('script', text=re.compile('{"ns":"pl\.content\.homeFeed\.index"')).get_text()
            html =  eval(html[html.find('(') + 1:html.rfind(')')])['html'].replace(r'\/', '/')
            html2 = urlopen(url2).read().decode(_CHARSET, errors='ignore')
            html2 = eval(html2)['data'].replace(r'\/', '/')
            html3 = urlopen(url3).read().decode(_CHARSET, errors='ignore')
            html3 = eval(html3)['data'].replace(r'\/', '/')
            change_user()
            time.sleep(INTERVAL)
            try_ = 3
            return ignore_emoji(html + html2 + html3)
        except:
            current_user = get_current_user()
            tag = test_cookie(current_user)
            if tag:
                if not try_:raise
                try_ -= 1
            change_user()
            if not tag:
                delete_cookie(current_user)
def get_id(soup):
    return soup['mid']
def match_item(soup):
    mid = get_id(soup)
    uid = re.search('id=(\\d+)', soup.find('a', {'usercard':True})['usercard']).group(1)
    content = soup.find('div', {'node-type':'feed_list_content'}).get_text()
    
    forward_soup = soup.find('div', {'node-type':'feed_list_forwardContent'})
    forward_uid = forward_content = None
    if forward_soup:
        date = eval(soup.find_all('a', {'node-type':'feed_list_item_date'})[-1]['date'])/1000
        try:
            forward_uid = re.search('id=(\\d+)', forward_soup.find('a', {'usercard':True})['usercard']).group(1)
            forward_content = forward_soup.find('div', 'feed_list_reason').get_text()
        except:
            pass
    else:
        date = eval(soup.find('a', {'node-type':'feed_list_item_date'})['date'])/1000
    
    action_soup = soup.find('ul', 'WB_row_line WB_row_r4 clearfix S_line2')
    if action_soup:
        temp = str(action_soup)
        try:
            report_count = re.search(re.compile('转发 (\\d+)'), temp).group(1)
        except:
            report_count = '0'
        try:
            comment_count = re.search(re.compile('评论 (\\d+)'), temp).group(1)
        except:
            comment_count = '0'
        zan_count = action_soup.find_all('em')[-1].get_text()
        if not zan_count:
            zan_count = '0'
    else:
        report_count = comment_count = zan_count = '0'
    return Weibo(mid, uid, content, date, report_count, comment_count, zan_count, forward_uid, forward_content)
def crawl(page_id, domain, todo, store_args, pages=None):
    page = 1
    html = _crawl_page(page_id, domain, page)
    soup = Soup(html)
    if not pages:
        try:
            pages = len(soup.find('div',{'node-type':'feed_list_page'}).ul.select('li'))
        except:
            pages = 1
    while True:
        if DEBUG:print(page, pages)
        weibos_source_list = soup.find_all('div', {'action-type':'feed_list_item'})
        if weibos_source_list:
            todo(weibos_source_list, store_args)
        page += 1
        if page > pages:break
        try:
            soup = Soup(_crawl_page(page_id, domain, page))
        except:
            if DEBUG:raise
            break
if __name__ == '__main__':
    page_id = '10080895c4665f1b8aeabd08859346aceaea41'
    domain = page_id[:6]
    from web.weibo.sina import auto_login
    auto_login('270121740@qq.com')
    print(_crawl_page(page_id, domain, 1))