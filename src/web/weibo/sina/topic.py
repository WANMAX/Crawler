'''
Created on 2016年1月27日

@author: wan
'''
from urllib import request
from web.weibo.sina import urlopen, INTERVAL
from web.weibo.sina.content import _crawl_page as crawl_page_weibo, match_item as match_weibo
from bs4 import BeautifulSoup as Soup
import re
from util.class_ import Topic
import time

_TOPIC_URL = 'http://d.weibo.com/100803_ctg1_1_-_ctg11?pids=Pl_Discover_Pt6Rank__4&Pl_Discover_Pt6Rank__4_filter=hothtlist_type=1&ajaxpagelet=1&Pl_Discover_Pt6Rank__4_page=%u'

def _get_topic_params(topic_url=None, topic_name=None):
    if not topic_url:
        if not topic_name:raise Exception()
        topic_url = 'http://huati.weibo.com/k/%s'%request.quote(topic_name)
    html = urlopen(topic_url).read().decode('utf-8', errors='ignore')
    page_id = re.search(re.compile("CONFIG\['page_id'\]='([^']+)'"), html).group(1)
    domain = page_id[:6]
    soup = Soup(html)
    html2 = soup.find('script', text=re.compile('FM\.view\({"ns":"","domid":"Pl_Third_Inline__3')).text
    html2 = eval(html2[html2.find('(')+1:html2.rfind(')')])['html'].replace('\\/', '/')
    soup2 = Soup(html2)
    introduction = soup2.text.strip()[len('导语：'):]
    return page_id, domain, introduction
def get_topic_name(soup):
    return soup.find('a', class_='S_txt1').text.strip()[1:-1]
def get_item(soup, topic_type):
    try:
        info_a = soup.find('a', class_='S_txt1')
        topic_name = info_a.text.strip()[1:-1]
        topic_url = info_a['href']
        page_id, domain, topic_introduction = _get_topic_params(topic_url)
        topic_args = (page_id, domain)
        weibo_div = Soup(crawl_page_weibo(page_id, domain, 1)).find('div', {'action-type':'feed_list_item'})
        if not weibo_div:topic_datetime = time.time()
        else:topic_datetime = match_weibo(weibo_div).time
        time.sleep(INTERVAL)
        return Topic(topic_name, topic_datetime, topic_type, topic_introduction, topic_args)
    except:
        return None
def _format_number(number_str):
    if number_str[-1] == '万':
        return eval(number_str[:-1])*10000
    elif number_str[-1] == '亿':
        return eval(number_str[:-1])*1000000000
    else:
        return eval(number_str)
def crawl(todo, store_args):
    topic_type = '社会'
    page = 1
    while True:
        html = urlopen(_TOPIC_URL%page).read().decode('utf-8')
        try:
            html = eval(html[html.find('{'):html.rfind('}')+1])['html'].replace('\\/', '/')
        except:
            page += 1
            if page > 150:break
            continue
        soup = Soup(html)
        divs = soup.find_all('li', class_='pt_li S_line2')
        if not divs:
            break
        divs = [item for item in divs if _format_number(item.find_all('span', class_='number')[-1].text.strip()) > 300000]
        store_args2 = list(store_args)
        store_args2.append(topic_type)
        todo(divs, store_args2)
        page += 1
        time.sleep(INTERVAL)
if __name__ == '__main__':
    from web.weibo.sina import auto_login
    auto_login()
    def todo(list_, nouse):
        for item in list_:
            print(get_item(item))
    crawl(todo, [])