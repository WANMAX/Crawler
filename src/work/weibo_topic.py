'''
Created on 2016年1月27日

@author: wan
'''
import __init__
import web.weibo
import store.weibo
import importlib
import logging.config

TOPIC_LIST = []
counter = 0
def _match_and_store(topic_module, store_module, content_module, weibo_module_str):
    def todo(source_list, store_args):
        result = [content_module.match_item(source_code) for source_code in source_list[:5]]
        store_module.store_weibos(result, store_args)
    def todo2(topic_list, store_args):
        result = [topic_module.get_item(item, store_args[1]) for item in topic_list if store_module.test_topic(topic_module.get_topic_name(item), store_args[0])]
        result = [item for item in result if item]
        store_module.store_topics(result, store_args)
        for topic in result:
            print(topic.topic_name)
            store_args = (weibo_module_str, topic.topic_name)
            page_id, domain = topic.topic_args
            try:
                content_module.crawl(page_id, domain, todo, store_args, 1)
            except:pass
        global counter
        counter += len(topic_list)
        print(counter)
    return todo2
def work(weibo_module_str, store_module_str):
    logger = logging.getLogger('crawlerLog')
    logger.info("'%s' weibo_topic start"%weibo_module_str)
    logger.info("'%s' auto login start"%weibo_module_str)
    weibo_module = importlib.import_module(web.weibo._WEIBO_MODULE_PATH%weibo_module_str)
    weibo_module.login_all_default_user()
    logger.info("'%s' auto login end"%weibo_module_str)
    store_args = (weibo_module_str, )
    logger.info("'%s' topic_crawler start"%weibo_module_str)
    topic_module = importlib.import_module(web.weibo._WEIBO_MODULE_PATH%weibo_module_str+'.topic')
    store_module = importlib.import_module(store.weibo._STORE_MODULE_PATH%store_module_str)
    content_module = importlib.import_module(web.weibo._WEIBO_MODULE_PATH%weibo_module_str+'.content')
    topic_module.crawl(_match_and_store(topic_module, store_module, content_module, weibo_module_str), store_args)
    logger.info("'%s' topic_crawler end"%weibo_module_str)
    global counter
    counter = 0
    logger.info("'%s' weibo_topic end"%weibo_module_str)

if __name__ == '__main__':
    logging.config.fileConfig('../logging_config.conf')
    work('sina', 'file_')