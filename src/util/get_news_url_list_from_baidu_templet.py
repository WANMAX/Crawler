'''
Created on 2015年11月11日

@author: wan
'''
import time
from util.urlopen_and_read import urlopen_and_read
from bs4 import BeautifulSoup as Soup
import re

def get_mothed(web_, url_pat):
    if web_.find(':') != -1:
        web_ = web_[web_.find(':')+3:]
    if web_.find('/') != -1:
        web_ = web_[:web_.find('/')]
    
    def get_news_url_list(date_=None):
        if not date_:
            time_ = time.localtime()
            time1 = time.mktime((time_[0], time_[1], time_[2]-1, 0, 0, 0, 0, 0, 0))
            time2 = time.mktime((time_[0], time_[1], time_[2]-1, 23, 59, 59, 0, 0, 0))
        else:
            time_ = time.strptime(date_,"%Y%m%d")
            time1 = time.mktime((time_[0], time_[1], time_[2], 0, 0, 0, 0, 0, 0))
            time2 = time.mktime((time_[0], time_[1], time_[2], 23, 59, 59, 0, 0, 0))
        _YESTODAY_URL_PAT = 'http://news.baidu.com/ns?bt=%u&et=%u&tn=newstitledy&rn=50&q6=%s'%(time1, time2, web_)+'&pn=%u'
        list_ = []
        pn = 0
        while True:
            web = _YESTODAY_URL_PAT%pn
            html = urlopen_and_read(web).decode('utf-8')
            soup = Soup(html)
            div_list = soup.find_all('div', class_='result')
            for div in div_list:
                web = div.a['href']
                if re.match(url_pat, web):
                    if '?' in web:
                        web = web[:web.find('?')]
                    if not web in list_:
                        list_.append(web)
            if not re.search('下一页', html):
                break
            pn += 50
        return {'':list_}
    return get_news_url_list