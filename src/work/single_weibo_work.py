'''
Created on 2015年11月16日

@author: wan
'''
import __init__
import logging.config
import importlib
import store.weibo
from store.weibo.file_ import STORE_DIR, _CHARSET
import os
import web.weibo
'''
from util.class_ import Weibo, Comment
import time
def init():
    def weibo_str(self):
        if self.forward_uid:
            return  "<weibo><mid>%s</mid><uid>%s</uid><text>%s</text><weiboDate>%s</weiboDate>\
<repostCount>%s</repostCount><commentCount>%s</commentCount><zanCount>%s</zanCount>\
<ruid>%s</ruid><originText>%s</originText></weibo>"\
% (self.mid, self.uid, self.content, time.strftime('%Y-%m-%d %H:%M', time.localtime(self.time)), self.repost_count, self.comment_count
   , self.zan_count, self.forward_uid, self.forward_content)
        else:
            return "<weibo><mid>%s</mid><uid>%s</uid><text>%s</text><weiboDate>%s</weiboDate>\
<repostCount>%s</repostCount><commentCount>%s</commentCount><zanCount>%s</zanCount></weibo>"\
 % (self.mid, self.uid, self.content, time.strftime('%Y-%m-%d %H:%M', time.localtime(self.time)), self.repost_count, self.comment_count, self.zan_count)
    Weibo.__str__ = weibo_str
''' 

MID_LIST = []
DEBUG = False

def _match_and_store(weibo_module_str, type_, work_module, store_module, result_mids=None):
    def method(source_list, store_args):
        if type_ == 'content':
            store_dir = STORE_DIR%weibo_module_str + 'source_code/%s/'%type_
            store_path = store_dir + '%s.txt'%store_args[1]
        else:
            store_dir = STORE_DIR%weibo_module_str + 'source_code/%s/%s/'%(type_, store_args[1])
            store_path = store_dir + '%s.txt'%store_args[2]
        os.makedirs(store_dir, exist_ok=True)
        source_list_bak = source_list
        if result_mids and type_ == 'content':
            global MID_LIST
            if not MID_LIST:
                MID_LIST = list(result_mids)
            source_list = [item for item in source_list if not work_module.get_id(item) in MID_LIST]
        content = '\n'.join([str(temp) for temp in source_list])
        if content:
            if  os.path.exists(store_path):
                with open(store_path, 'a', encoding=_CHARSET, errors='ignore') as file:
                    file.write('\n'+content)
            else:
                with open(store_path, 'w', encoding=_CHARSET, errors='ignore') as file:
                    file.write(content)
        result = [work_module.match_item(source_code) for source_code in source_list_bak]
        if type_ == 'content':
            store_module.store_weibos(result, store_args)
        elif type_ == 'comment':
            store_module.store_comments(result, store_args)
        elif type_ == 'repost':
            store_module.store_reposts(result, store_args)
    return method
def _work_content(weibo_module_str, content_module, store_module, topic_name, page_id, domain, store_args, logger):
    try:
        result_mids = store_module.get_result_mids(store_args)
        content_module.crawl(page_id, domain, _match_and_store(weibo_module_str, 'content', content_module, store_module, result_mids), store_args)
    except Exception as e:
        logger.error("\"%s\" happened on '%s' '%s' work_content"%(e, weibo_module_str, topic_name))
        if DEBUG:
            raise
        raise Exception()
def _work_comment(weibo_module_str, store_module, mid, topic_name, store_args, logger, counter):
    try:
        store_path = STORE_DIR%weibo_module_str + 'source_code/comment/%s/%s.txt'%(store_args[1], store_args[2])
        if os.path.exists(store_path):
            os.remove(store_path)
        comment_module = importlib.import_module(web.weibo._WEIBO_MODULE_PATH%weibo_module_str+'.comment')
        comment_module.crawl(mid, _match_and_store(weibo_module_str, 'comment', comment_module, store_module), store_args, counter)
    except Exception as e:
        logger.error("\"%s\" happened on '%s' '%s' work_comment"%(e, weibo_module_str, mid))
        if DEBUG:
            raise
        raise Exception()
def _work_repost(weibo_module_str, store_module, mid, topic_name, store_args, logger, counter):
    try:
        store_path = STORE_DIR%weibo_module_str + 'source_code/repost/%s/%s.txt'%(store_args[1], store_args[2])
        if os.path.exists(store_path):
            os.remove(store_path)
        repost_module = importlib.import_module(web.weibo._WEIBO_MODULE_PATH%weibo_module_str+'.repost')
        repost_module.crawl(mid, _match_and_store(weibo_module_str, 'repost', repost_module, store_module), store_args, counter)
    except Exception as e:
        logger.error("\"%s\" happened on '%s' '%s' work_repost"%(e, weibo_module_str, mid))
        if DEBUG:
            raise
        raise Exception()
def work(weibo_module_str, store_module_str, counter=None):    
    store_module = importlib.import_module(store.weibo._STORE_MODULE_PATH%store_module_str)
    logger = logging.getLogger('crawlerLog')
    logger.info("'%s' single_weibo_work start"%weibo_module_str)
    logger.info("'%s' auto login start"%weibo_module_str)
    weibo_module = importlib.import_module(web.weibo._WEIBO_MODULE_PATH%weibo_module_str)
    weibo_module.login_all_default_user()
    logger.info("'%s' auto login end"%weibo_module_str)
    content_module = importlib.import_module(web.weibo._WEIBO_MODULE_PATH%weibo_module_str+'.content')
    for item in store_module.get_topics(weibo_module_str):
        try:
            topic_name, topic_args = item.topic_name, item.topic_args
            page_id, domain = topic_args
            logger.info("'%s' topic '%s'"%(weibo_module_str, topic_name))
            logger.info("'%s' work_content start"%weibo_module_str)
            global MID_LIST
            MID_LIST = []
            store_args = (weibo_module_str, topic_name)
            _work_content(weibo_module_str, content_module, store_module, topic_name, page_id, domain, store_args, logger)
            logger.info("'%s' work_content end"%weibo_module_str)
            logger.info("'%s' work_comment_and_repost start"%weibo_module_str)
            for mid in store_module.get_mids(store_args):
                store_args = (weibo_module_str, topic_name, mid)
                _work_comment(weibo_module_str, store_module, mid, topic_name, store_args, logger, counter)
                _work_repost(weibo_module_str, store_module, mid, topic_name, store_args, logger, counter)
            logger.info("'%s' work_comment_and_repost end"%weibo_module_str)
        except Exception as e:
            if e:
                logger.error("\"%s\" happened on '%s'"%(e, weibo_module_str))
            if DEBUG:
                raise
        if topic_name in dir() and topic_name:
            store_module.end((weibo_module_str, topic_name))
    logger.info("'%s' single_weibo_work end"%weibo_module_str)
if __name__ == '__main__':
    logging.config.fileConfig('../logging_config.conf')
    from util.counter import Counter
    counter = Counter(logging.getLogger('crawlerLog'), 10)
    work('sina', 'database', counter, '美哭了的泼水成冰')
