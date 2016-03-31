'''
Created on 2015年11月6日

@author: wan
'''
import __init__
from util.urlopen_and_read import urlopen_and_read
import logging.config
import importlib
import web.news
import re
import store.news
from store.news.file_ import STORE_DIR, _CHARSET
import os
from util import thread_pool
from __init__ import WORK_PATH

NAME_PAT = '/|\\\\|:|\\*|\"|<|>|\\|'
TRY_TIME = 10
DEBUG = True

def _match_and_store_comments(news_module_str, news_module, store_module):
    def method(comment_source_list, store_args):
        store_dir = STORE_DIR%news_module_str + 'comments_source_code/'
        os.makedirs(store_dir, exist_ok=True)
        store_path = store_dir + '%s.txt'%store_args[2]
        content = '\n'.join([str(temp) for temp in comment_source_list])
        if not DEBUG:
            if  os.path.exists(store_path):
                with open(store_path, 'a', encoding=_CHARSET, errors='ignore') as file:
                    file.write('\n'+content)
            else:
                with open(store_path, 'w', encoding=_CHARSET, errors='ignore') as file:
                    file.write(content)
        comments = [news_module.match_comment(comment_source_code) for comment_source_code in comment_source_list]
        if not DEBUG:
            store_module.store_comments(comments, store_args)
    return method

def _work_item(news_module_str, store_module, news_module, type_, url, logger):
    if DEBUG:
        print(url)
    try:
        try_ = TRY_TIME
        while True:
            try:
                html = urlopen_and_read(url).decode(news_module.NEWS_CHARSET, 'ignore')
                news = news_module.match_news(html, url)
                if not news:return
                break
            except:
                if try_:
                    try_ -= 1
                    continue
                else:
                    raise
        file_name = re.sub(NAME_PAT, '', news.title)
        if not type_:
            try:
                type_ = news_module.get_type(html)
            except:
                type_ = 'temp'
        store_args = news_module_str, type_, file_name
        if not DEBUG:
            store_module.store_news(news, store_args)
        comment_url_args = news.comment_url_args
        web.news.crawl_comments(news_module, _match_and_store_comments(news_module_str, news_module, store_module), store_args, comment_url_args)
    except Exception as e:
        logger.error("\"%s\" happened on '%s' '%s' work_item"%(e, news_module_str, url))
        if DEBUG:
            raise

def work(news_module_str, store_module_str, date_=None):
    logger = logging.getLogger('crawlerLog')
    logger.info("'%s' single_news_work start"%news_module_str)
    news_module = importlib.import_module(web.news._NEWS_MODULE_PATH%news_module_str)
    logger.info("'%s' get_news_url_list start"%news_module_str)
    list_ = news_module.get_news_url_list(date_)
    logger.info("'%s' get_news_url_list end"%news_module_str)
    logger.info("'%s' work_item start"%news_module_str)
    store_module = importlib.import_module(store.news._STORE_MODULE_PATH%store_module_str)
    for type_ in list_:
        for url in list_[type_]:
            thread_pool.add(_work_item, (news_module_str, store_module, news_module, type_, url, logger))
    thread_pool.start()
    thread_pool.join()
    logger.info("'%s' work_item end"%news_module_str)
    logger.info("'%s' single_news_work end"%news_module_str)

if __name__ == '__main__':
    logging.config.fileConfig('%s/logging_config.conf'%WORK_PATH)
    date = '201603%02u'
    start = 31
    stop = 31
    while start <= stop:
        date2 = date%start
        start += 1
        print(date2)
        for module_str in ['wangyi']:
            work(module_str, 'database', date2)
