'''
Created on 2015年11月5日

@author: wan
'''

from util.urlopen_and_read import urlopen_and_read
from util.class_ import News, Comment
from bs4 import BeautifulSoup as Soup
import re
import time
from util.dict_extra import true, false
from web.news import BY_PAGE

NEWS_CHARSET='gb2312'
COMMENT_CHARSET='utf-8'
TYPE=BY_PAGE
_NEWS_URL_TYPE_PAT_DICT = {'国内':'http://news.sohu.com/guoneixinwen%s.shtml', '国际':'http://news.sohu.com/guojixinwen%s.shtml',
                           '社会':'http://news.sohu.com/shehuixinwen%s.shtml'}

def _get_news_url_list_by_pat_and_date(pat, date):
    list_ = []
    tag = False
    html = urlopen_and_read(pat%'', ).decode('gbk', 'ignore')
    page = eval(re.search('var maxPage = (\\d+);', html).group(1))
    soup = Soup(html)
    while True:
        for div in soup.find_all('div', class_='article'):
            url = div.find_all('a')[1]['href']
            if url[21:29] > date:
                continue
            elif url[21:29] == date:
                if '?' in url:
                    url = url[:url.find('?')]
                if not url in list_:
                    list_.append(url)
            else:
                tag = True
                break
        page -= 1
        if tag:
            break
        soup = Soup(urlopen_and_read(pat%'_%u'%page).decode('gbk', 'ignore'))
    return list_
def get_news_url_list(date_=None):
    if not date_:
        today = time.localtime()
        date_ = time.strftime('%Y%m%d', (today[0], today[1], today[2]-1, today[3], today[4], today[5], today[6], today[7], today[8]))
    dict_ = {}
    for type_ in _NEWS_URL_TYPE_PAT_DICT:
        dict_[type_] = _get_news_url_list_by_pat_and_date(_NEWS_URL_TYPE_PAT_DICT[type_], date_)
    return dict_
def match_news(html, url):
    soup = Soup(html)
    sid = re.search('/n(\\d+)', url).group(1)
    url2 = 'http://changyan.sohu.com/node/html?client_id=cyqemw6s1&topicsid=%s' % sid
    topic_id = eval(urlopen_and_read(url2).decode('utf-8', 'ignore'))['listData']['topic_id']
    comment_url_args = (topic_id,)
    title = soup.title.text
    main_content = soup.find('div',{'itemprop':'articleBody'})
    if not main_content:return
    if main_content.img:
        news_image = main_content.img['src']
    else:
        news_image = None
    content = '\n'.join([temp.strip() for temp in [item.get_text() for item in main_content.find_all('p')] if not re.match('\\s*$', temp)])
    source = soup.find('span', {'itemprop':'name'}).text
    source_url = soup.find('span',{'itemprop':'isBasedOnUrl'}).text
    date = soup.find('div', {'itemprop':'datePublished'}).get_text()
    date = time.strptime(date,"%Y-%m-%d %H:%M:%S")
    date = time.mktime(date)
    return News(url, comment_url_args, title, content, source, date, source_url, news_image=news_image)
def get_comment_page_url(page, args):
    topic_id = args[0]
    url = 'http://changyan.sohu.com/api/2/topic/comments?client_id=cyqemw6s1&topic_id=%s' % topic_id
    if page == 1:
        return url
    return url + '&page_no=%u'%page
def get_comment_source_list(html):
    return eval(html)['comments']
def match_comment(comment_source_code):
    userid = 'sh%s'%comment_source_code['user_id']
    content = comment_source_code['content'].strip()
    time_ = comment_source_code['create_time']/1000
    location = comment_source_code['ip_location']
    vote = comment_source_code['support_count']
    return Comment(userid, content, time_, location, vote)