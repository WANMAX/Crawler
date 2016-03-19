'''
Created on 2016年1月11日

@author: wan
'''

from bs4 import BeautifulSoup as Soup
from web.news import BY_PAGE
from util.class_ import News, Comment
import re
import time
from util.dict_extra import true, false, null
from util.urlopen_and_read import urlopen_and_read

DICT = {0: "国内", 1: "国际", 2: "社会", 4: "探索", 5: "军事"}
NEWS_CHARSET = 'gbk'
COMMENT_CHARSET = 'utf-8'
TYPE=BY_PAGE

def get_news_url_list(date_=None):
    if not date_:
        today = time.localtime()
        date_ = time.strftime('%Y-%m-%d', (today[0], today[1], today[2]-1, today[3], today[4], today[5], today[6], today[7], today[8]))
    else:
        date_ = time.strptime(date_,"%Y%m%d")
        date_ = time.strftime('%Y-%m-%d', (date_[0], date_[1], date_[2], date_[3], date_[4], date_[5], date_[6], date_[7], date_[8]))
    data = urlopen_and_read("http://news.163.com/special/0001220O/news_json.js").decode("gbk", 'ignore')
    data = eval(data[data.find('{'):data.rfind('}')+1])
    data = data['news']
    dict_ = {}
    for newsData in data:
        try:
            type_ = DICT[newsData[0]['c']]
        except:
            continue 
        dict_[type_] = []
        for newsDataItem in newsData:
            if newsDataItem['p'][0:10] > date_:
                continue
            elif newsDataItem['p'][0:10] == date_:
                url = newsDataItem['l']
                if '?' in url:
                    url = url[:url.find('?')]
                if not url in dict_[type_]:
                    dict_[type_].append(url)
            else:
                break
    return dict_
def match_news(html, url):
    soup = Soup(html)
    main_text = soup.find('div', {'id':'endText'})
    if not main_text:return
    if main_text.img:
        news_image = main_text.img['src']
    else:
        news_image = None
    content = '\n'.join([item.text.strip() for item in main_text.find_all('p')])
    date_source_div =  soup.find('div', class_=re.compile('ep-time-soure'))
    if not date_source_div:return
    source_a = date_source_div.a
    source_url =  source_a['href']
    source = source_a.text
    date = date_source_div.text.strip().split(' ')[0]
    date = time.strptime(date,"%Y-%m-%d")
    date = time.mktime(date)
    title = soup.title.text
    title = title[:title.rfind('_')]
    thread_id = re.search('threadId = "(\\S+?)"', html).group(1)
    comment_url_args = (thread_id, )
    return News(url, comment_url_args, title, content, source, date, source_url, news_image=news_image)
PAGE_COMMENTS_NUM = 30
def get_comment_page_url(page, args):
    offset = (page - 1) * PAGE_COMMENTS_NUM
    thread_id = args[0]
    return 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s/comments/newList?offset=%u&limit=%u'%(thread_id, offset, PAGE_COMMENTS_NUM) 
def get_comment_source_list(html):
    comments_dict =  eval(html)['comments']
    comments_list = []
    for comment_id in comments_dict.keys():
        item_dict = comments_dict[comment_id]
        comments_list.append(item_dict)
    return sorted(comments_list, key=lambda x:x['createTime'], reverse=True)
def match_comment(comment_source_code):
    user_info = comment_source_code['user']
    userid = 'wy%s'%user_info['userId']
    location = user_info['location']
    content = comment_source_code['content'].strip()
    time_ = comment_source_code['createTime']
    time_ = time.strptime(time_,"%Y-%m-%d %H:%M:%S")
    time_ = time.mktime(time_)
    vote = comment_source_code['vote']
    return Comment(userid, content, time_, location, vote)
