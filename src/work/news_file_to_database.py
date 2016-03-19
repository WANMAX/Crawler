'''
Created on 2016年1月15日

@author: wan
'''
import __init__
from store.news import file_, database
import re
import os
from util import thread_pool
from threading import Thread

def do_item(path):
    news_module_str = re.search('news/(\\S+?)/', path).group(1)
    type_ = re.search('result/(\\S+?)/', path).group(1)
    try:
        file_name = re.search('%s/(\\S+?)\.txt'%type_, path).group(1)
    except:
        file_name = re.search('%s/(\\S+)'%type_, path).group(1)
    store_args = (news_module_str, type_, file_name)
    news = file_.read_news(path)
    database.store_news(news, store_args)
    comments = file_.read_comments(path)
    database.store_comments(comments, store_args)
    os.remove(path)
DIR = file_.STORE_DIR
DIR = DIR[:DIR.rfind('%')]
def _get_list_item():
    for web in os.listdir(DIR):
        type_path = '%s%s/result'%(DIR, web)
        for type in os.listdir(type_path):
            item_path = '%s/%s'%(type_path, type)
            for item in os.listdir(item_path):
                yield Thread(target=do_item, args=('%s/%s'%(item_path, item),))
def do():
    thread_pool.set_generator(_get_list_item())
    thread_pool.start()
    thread_pool.join()

if __name__ == '__main__':
    do()
