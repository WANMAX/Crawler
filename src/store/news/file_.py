'''
Created on 2015年11月7日

@author: wan
'''

import os
from util.class_ import News, Comment
from bs4 import BeautifulSoup as Soup
import time

STORE_DIR = os.path.dirname(os.path.realpath(__file__))
STORE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(STORE_DIR)))
STORE_DIR = '%s/news/'%STORE_DIR+'%s/'
_CHARSET = 'utf-8'

def store_news(news, store_args):
    store_dir = STORE_DIR%store_args[0]+'result/%s/'%store_args[1]
    os.makedirs(store_dir, exist_ok=True)
    with open(store_dir + store_args[2] + '.txt', 'w', encoding=_CHARSET, errors='ignore') as file:
        file.write(str(news))
    
def store_comments(comments, store_args):
    content = '\n'.join([str(item) for item in comments])
    store_path = STORE_DIR%store_args[0]+'result/%s/%s.txt'%(store_args[1], store_args[2])
    with open(store_path, 'a', encoding=_CHARSET, errors='ignore') as file:
        file.write('\n'+content)

def _get_time(text):
    time_ = time.strptime(text,"%Y-%m-%d")
    return time.mktime(time_)
def read_news(path):
    with open(path, 'r', encoding=_CHARSET, errors='ignore') as file:
        lines = ''
        for line in file:
            lines += line
            if '</news>' in line:
                break
        soup = Soup(lines)
        url = soup.url.text
        comment_url_args = eval(soup.comment_url_args.text)
        title = soup.title.text
        content = soup.content.text
        source = soup.source.text
        date = _get_time(soup.date.text)
        if soup.source_url:
            source_url = soup.source_url.text
        else:
            source_url = None
        if soup.author:
            author = soup.author.text
        else:
            author = None
        if soup.abstract:
            abstract = soup.abstract.text
        else:
            abstract = None
        if soup.news_image:
            news_image = soup.news_image.text
        else:
            news_image = None
        return News(url, comment_url_args, title, content, source, date, source_url, author, abstract, news_image)
    raise
def read_comments(path):
    with open(path, 'r', encoding=_CHARSET, errors='ignore') as file:
        start = False
        comment_lines = ''
        for line in file:
            if not start:
                if '</news>' in line:
                    start = True
                continue
            comment_lines += line
            if '</comment>' in line:
                soup = Soup(comment_lines)
                user_id = soup.user_id.text
                content = soup.content.text
                time_ = _get_time(soup.time.text)
                if soup.location:
                    location = soup.location.text
                else:
                    location = None
                if soup.vote:
                    vote = soup.vote.text
                else:
                    vote = None
                yield Comment(user_id, content, time_, location, vote)
                comment_lines = ''
        return
    raise