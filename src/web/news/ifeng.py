'''
Created on 2016年1月14日

@author: wan
'''

import time
from bs4 import BeautifulSoup as Soup
from util.urlopen_and_read import urlopen_and_read
from util.class_ import News, Comment
from web.news import BY_PAGE

DICT_ = {'大陆':'11528', '国际':'11574', '台湾':'11490', '社会':'7837'}
URL_PAT = 'http://news.ifeng.com/listpage/%s/%s/%u/rtlist.shtml'

COMMENT_CHARSET = NEWS_CHARSET = 'utf-8'
TYPE = BY_PAGE

def get_news_url_list(date=None):
    if not date:
        today = time.localtime()
        date = time.strftime('%Y%m%d', (today[0], today[1], today[2]-1, today[3], today[4], today[5], today[6], today[7], today[8]))
    dict_ = {}
    for type_ in DICT_.keys():
        type_id = DICT_[type_]
        page = 1
        while True:
            url_ = URL_PAT%(type_id, date, page)
            try:
                soup = Soup(urlopen_and_read(url_).decode('utf-8'))
                url_list = [item['href'] for item in soup.find('div', class_='newsList').ul.find_all('a')]
            except:
                break
            if not type_ in dict_.keys():
                dict_[type_] = []
            dict_[type_].extend(url_list)
            page += 1
    return dict_
def match_news(html, url_):
    soup = Soup(html)
    title = soup.title.text
    if '|' in title:
        title = title[:title.find('|')]
    else:
        title = title[:title.rfind('_')]
    main_content = soup.find('div', id='main_content')
    if not main_content:return
    content = '\n'.join([item.text.strip() for item in main_content.find_all('p')])
    if main_content.img:
        news_image = main_content.img['src']
    else:
        news_image = None
    source_span = soup.find('span', {'itemprop':'name'})
    source = source_span.text
    try:
        source_url = source_span.a['href']
    except:
        source_url = None
    time_ = soup.find('span', {'itemprop':'datePublished'}).get_text()
    time_ = time.strptime(time_,"%Y年%m月%d日 %H:%M")
    time_ = time.mktime(time_)
    data = {'docurl':url_}
    comment_url_args = (data)
    return News(url_, comment_url_args, title, content, source, time_, source_url, news_image=news_image)
def get_comment_page_url(page, args):
    args['p'] = str(page)
    return 'http://comment.ifeng.com/get?job=1&order=DESC&orderBy=create_time&format=json&pagesize=20', args
def get_comment_source_list(html):
    return eval(html)['comments']
def match_comment(comment_source_code):
    userid = 'fh%s'%comment_source_code['user_id']
    content = comment_source_code['comment_contents'].strip()
    time_ = eval(comment_source_code['create_time'])
    location = comment_source_code['ip_from']
    vote = comment_source_code['uptimes']
    return Comment(userid, content, time_, location, vote)
