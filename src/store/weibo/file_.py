'''
Created on 2015年11月16日

@author: wan
'''
import os

STORE_DIR = os.path.dirname(os.path.realpath(__file__))
STORE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(STORE_DIR)))
STORE_DIR = '%s/weibo/'%STORE_DIR+'%s/'
_CHARSET = 'utf-8'
from bs4 import BeautifulSoup as Soup


def get_mids(store_args):
    path = STORE_DIR%store_args[0]+'temp/%s/weibo.txt'%store_args[1]
    with open(path, 'r', encoding=_CHARSET, errors='ignore') as file:
        for line in file:
            yield line[line.find('mid>')+4: line.find('</mid')]
    result_mids = get_result_mids(store_args)
    if not result_mids:return
    for item in result_mids:
        yield item
def get_result_mids(store_args):
    path = STORE_DIR%store_args[0]+'result/'
    if os.path.exists(path) and store_args[1] in os.listdir(path):
        result_file = STORE_DIR%'sina'+'result/%s/weibo.txt'%store_args[1]
    else:
        return
    with open(result_file, 'r', encoding=_CHARSET, errors='ignore') as file:
        for line in file:
            yield line[line.find('mid>')+4: line.find('</mid')]
def store_weibos(weibos, store_args):
    if not weibos:
        return
    content = '\n'.join([str(item) for item in weibos])
    store_dir = STORE_DIR%store_args[0]+'temp/%s/'%store_args[1]
    os.makedirs(store_dir, exist_ok=True)
    store_path = store_dir+'weibo.txt'
    store_path2 = STORE_DIR%store_args[0]+'result/%s/weibo.txt'%store_args[1]
    if os.path.exists(store_path2):
        line_list = []
        weibo_list = [item.mid for item in weibos]
        change = False
        with open(store_path2, 'r', encoding=_CHARSET, errors='ignore') as file:
            line_list = []
            for line in file:
                if not line[line.find('mid>')+4:line.find('</mid')]  in weibo_list:
                    line_list.append(line)
                else:
                    change = True
        if change:
            with open(store_path2, 'w', encoding=_CHARSET, errors='ignore') as file:
                file.write('\n'.join(line_list))
    if os.path.exists(store_path):
        with open(store_path, 'a', encoding=_CHARSET, errors='ignore') as file:
            file.write('\n'+content)
    else:
        with open(store_path, 'w', encoding=_CHARSET, errors='ignore') as file:
            file.write(content)
def store_comments(comments, store_args):
    if not comments:
        return
    content = '\n'.join([str(item) for item in comments])
    store_dir = STORE_DIR%store_args[0]+'temp/%s/comment/'%store_args[1]
    os.makedirs(store_dir, exist_ok=True)
    store_path = store_dir+'%s.txt'%store_args[2]
    if os.path.exists(store_path):
        with open(store_path, 'a', encoding=_CHARSET, errors='ignore') as file:
            file.write('\n'+content)
    else:
        with open(store_path, 'w', encoding=_CHARSET, errors='ignore') as file:
            file.write(content)
def store_reposts(reposts, store_args):
    if not reposts:
        return
    content = '\n'.join([str(item) for item in reposts])
    store_dir = STORE_DIR%store_args[0]+'temp/%s/repost/'%store_args[1]
    os.makedirs(store_dir, exist_ok=True)
    store_path = store_dir+'%s.txt'%store_args[2]
    if os.path.exists(store_path):
        with open(store_path, 'a', encoding=_CHARSET, errors='ignore') as file:
            file.write('\n'+content)
    else:
        with open(store_path, 'w', encoding=_CHARSET, errors='ignore') as file:
            file.write(content)
def _remove_not_empty_dir(path):
    for item in os.listdir(path):
        list_path = path+item
        if os.path.isdir(list_path):
            _remove_not_empty_dir(list_path)
        else:
            os.remove(list_path)
    os.rmdir(path)
def end(store_args):
    base_dir = STORE_DIR%store_args[0]+'temp/%s/'%store_args[1]
    store_path = base_dir + 'weibo.txt'
    store_dir2 = STORE_DIR%store_args[0]+'result/%s/'%store_args[1]
    store_path2 = store_dir2 + 'weibo.txt'
    os.makedirs(store_dir2, exist_ok=True)
    if os.path.exists(store_path):
        with open(store_path, 'r', encoding=_CHARSET, errors='ignore') as file:
            with open(store_path2, 'a', encoding=_CHARSET, errors='ignore') as file2:
                file2.write(file.read())
        os.remove(store_path)
    if len(os.listdir(store_dir2)) == 0:
        os.rmdir(store_dir2)
        return
    store_dir = STORE_DIR%store_args[0]+'temp/%s/comment/'%store_args[1]
    store_dir2 = STORE_DIR%store_args[0]+'result/%s/comment/'%store_args[1]
    os.makedirs(store_dir2, exist_ok=True)
    if os.path.exists(store_dir):
        for list_path in os.listdir(store_dir):
            list_path2 = store_dir2+list_path
            if os.path.exists(list_path2):
                os.remove(list_path2)
            os.rename(store_dir + list_path, list_path2)
    store_dir = STORE_DIR%store_args[0]+'temp/%s/repost/'%store_args[1]
    store_dir2 = STORE_DIR%store_args[0]+'result/%s/repost/'%store_args[1]
    os.makedirs(store_dir2, exist_ok=True)
    if os.path.exists(store_dir):
        for list_path in os.listdir(store_dir):
            list_path2 = store_dir2+list_path
            if os.path.exists(list_path2):
                os.remove(list_path2)
            os.rename(store_dir + list_path, list_path2)
    _remove_not_empty_dir(base_dir)
def test_topic(topic_name,  weibo_module_str):
    store_path = STORE_DIR%weibo_module_str+'result/topic'
    if os.path.exists(store_path):
        topic_name_len = len(topic_name)
        with open(store_path, 'r', encoding=_CHARSET, errors='ignore') as file:
            for line in file:
                try:
                    if line[19:19+topic_name_len] == topic_name:
                        return False
                except:
                    pass
    return True
def store_topics(topics, store_args):
    if not topics:return
    store_dir = STORE_DIR%store_args[0]+'result/'
    os.makedirs(store_dir, exist_ok=True)
    store_path = store_dir + 'topic'
    content = '\n'.join([str(item) for item in topics])
    if os.path.exists(store_path):
        with open(store_path, 'a', encoding=_CHARSET, errors='ignore') as file:
            file.write('\n'+content)
    else:
        with open(store_path, 'w', encoding=_CHARSET, errors='ignore') as file:
            file.write(content)
TOPIC_PATH = STORE_DIR+'result/topic'
TOPIC_PATH2 = TOPIC_PATH+'_active'
from util.class_ import Topic
def match_topic(html):
    soup = Soup(html)
    return Topic(soup.topic_name.text, eval(soup.topic_datetime.text), soup.topic_type.text, soup.topic_introduction.text, eval(soup.topic_args.text))
def get_topics(weibo_module_str):
    path = TOPIC_PATH2%weibo_module_str
    if not os.path.exists(path):return
    name_list = []
    with open(path, 'r', encoding=_CHARSET, errors='ignore') as file:
        for line in file:
            name_list.append(line.strip())
    path2 = TOPIC_PATH%weibo_module_str
    if not os.path.exists(path2):return
    with open(path2, 'r', encoding=_CHARSET, errors='ignore') as file:
        for line in file:
            topic = match_topic(line)
            if topic.topic_name in name_list:
                yield topic