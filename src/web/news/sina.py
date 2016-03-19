'''
Created on 2016年1月13日

@author: wan
'''
from util.urlopen_and_read import urlopen_and_read
import time
from bs4 import BeautifulSoup as Soup
import re
from util.class_ import News, Comment
from web.news import BY_PAGE

NEWS_CHARSET='utf-8'
COMMENT_CHARSET = 'gbk'
TYPE=BY_PAGE

NEWS_URL_DICT={
               '国内新闻':'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_all=1&show_num=22&tag=1&page=%u',
               '国际新闻':'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gjxw&level==1||=2&show_all=1&show_num=22&tag=1&page=%u',
               '社会新闻':'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=shxw&cat_2==zqsk||=qwys||=shwx||=fz-shyf&level==1||=2&show_all=1&show_num=22&tag=1&page=%u',
               }
def get_news_url_list(date_=None):
    if not date_:
        today = time.localtime()
        date_ = time.strftime('%Y%m%d', (today[0], today[1], today[2]-1, today[3], today[4], today[5], today[6], today[7], today[8]))
    dict_ = {}
    for type_ in NEWS_URL_DICT.keys():
        url = NEWS_URL_DICT[type_]
        page = 1
        tag = False
        while True:
            data = urlopen_and_read(url%page).decode("utf-8", 'ignore') 
            data = eval(data)['result']['data']
            for item in data:
                date = time.localtime(eval(item['createtime']))
                date = time.strftime('%Y%m%d', date)
                if date > date_:
                    continue
                elif date == date_:
                    if not type_ in dict_.keys():
                        dict_[type_] = []
                    url_ = item['url'].replace('\\', '')
                    if not 'video' in url_:
                        if '?' in url_:
                            url_ = url_[:url_.find('?')]
                        if not url_ in dict_[type_]:
                            dict_[type_].append(url_)
                else:  
                    tag = True
                    break
            if tag:
                break
            page += 1
    return dict_
def match_news(html, url):
    soup = Soup(html)
    title = soup.title.text
    title = title[:title.rfind('_')]
    main_content = soup.find('div', id='artibody')
    if not main_content:return
    if main_content.img:
        news_image = main_content.img['src']
    else:
        news_image = None
    content = '\n'.join([item.text.strip() for item in main_content.find_all('p')])
    date_source_span = soup.find('span', id='navtimeSource')
    time_ = re.split('\\s+', date_source_span.text.strip())[0]
    time_ = time.strptime(time_,"%Y年%m月%d日%H:%M")
    time_ = time.mktime(time_)
    source_a = date_source_span.a
    try:
        source = source_a.text
        source_url = source_a['href']
    except:
        source = '综合'
        source_url = None
    channel = re.search('channel: \'(\\S+?)\'', html).group(1)
    newsid = re.search('newsid: \'(\\S+?)\'', html).group(1)
    comment_url_args = (channel, newsid)
    return News(url, comment_url_args, title, content, source, time_, source_url, news_image=news_image)
def get_comment_page_url(page, args):
    channel = args[0]
    newsid = args[1]
    return 'http://comment5.news.sina.com.cn/page/info?format=json&channel=%s&newsid=%s&page=%u&page_size=20'%(channel, newsid, page)
def get_comment_source_list(html):
    return eval(html)['result']['cmntlist']
def match_comment(comment_source_code):
    userid = 'xl%s'%comment_source_code['uid']
    content = comment_source_code['content'].strip()
    time_ = comment_source_code['time']
    time_ = time.strptime(time_,"%Y-%m-%d %H:%M:%S")
    time_ = time.mktime(time_)
    location = comment_source_code['area']
    vote = eval(comment_source_code['agree'])
    return Comment(userid, content, time_, location, vote)
