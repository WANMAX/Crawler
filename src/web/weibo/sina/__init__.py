'''
Created on 2015年5月30日

@author: wan
'''

from util import PROXY
import base64
import rsa
import binascii
from http.cookiejar import LWPCookieJar
from urllib import request, parse
import time
import re
import os
from bs4 import BeautifulSoup as Soup

_COOKIE_PATH = "%s/cookie/"%os.path.dirname(os.path.realpath(__file__))
_TIME_INTERVAL = 3600 * 11
_CHARSET = 'utf-8'
_DEFAULT_USER = {'18819423713': 'b421573145', '270121740@qq.com': '13421573145', '18819423713@163.com': '13421573145', 'wanlqxcfz@qq.com': '13421573145', '18819423713@139.com': '13421573145', 'lhd1163405052@163.com': '13421573145'}
_CURRENT_USER = None
_EMOJI_FACE_PAT = re.compile('[\uD800-\uDBFF][\uDC00-\uDFFF]')
_HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}  
INTERVAL = 1
DEBUG = False
global cj

def get_current_user():
    return _CURRENT_USER

def init():
    global cj
    cj = LWPCookieJar()
    cookie_support = request.HTTPCookieProcessor(cj)
    if PROXY:
        try:
            from tool import proxy
            opener = proxy.build_opener(cookie_support , request.HTTPHandler)
        except:
            opener = request.build_opener(cookie_support , request.HTTPHandler)
    else:
        opener = request.build_opener(cookie_support , request.HTTPHandler)
    request.install_opener(opener)
def urlopen(url, post_data=None):
    if post_data:
        post_data = parse.urlencode(post_data).encode(_CHARSET)
    req = request.Request(url, post_data, _HEADERS)  
    return request.urlopen(req)
def ignore_emoji(html):
    return _EMOJI_FACE_PAT.sub('' ,html)
def get_login_time(username):
    if os.path.exists(_COOKIE_PATH + "timestamp"):
        with open(_COOKIE_PATH + "timestamp", 'r', encoding=_CHARSET) as file:
            html = file.read()
        soup = Soup(html)
        soup = soup.find('username', text=username)
        if soup:
            soup = soup.parent
            return eval(soup.time.get_text())
def save_cookie(username=_CURRENT_USER):
    if not os.path.exists(_COOKIE_PATH):
        os.makedirs(_COOKIE_PATH)
    cj.save(_COOKIE_PATH + "cookie_%s" % username, ignore_discard=True, ignore_expires=True)
    store_path = _COOKIE_PATH + "timestamp"
    if os.path.exists(store_path):
        with open(store_path, 'r', encoding=_CHARSET) as file:
            html = file.read()
        soup = Soup(html)
        soup = soup.find('username',text=username)
        if soup:
            soup = soup.parent
            soup.time.string = str(int(time.time()))
            with open(store_path, 'w', encoding=_CHARSET) as file:
                file.write(str(soup))
        else:
            with open(store_path, 'a', encoding=_CHARSET) as file:
                file.write("<timestamp><username>%s</username><time>%u</time></timestamp>" % (username, int(time.time())))
    else:
        with open(store_path, 'w', encoding=_CHARSET) as file:
            file.write("<timestamp><username>%s</username><time>%u</time></timestamp>" % (username, int(time.time())))
def load_cookie(username):
    init()
    cj.load(_COOKIE_PATH + "cookie_%s" % username, ignore_discard=True, ignore_expires=True)
    global _CURRENT_USER
    _CURRENT_USER = username
def test_cookie(username):
    if username == _CURRENT_USER:
        url = 'http://weibo.com/2863259912/AhMRtlt3M'
        try:
            res = urlopen(url).read()
            html = res.decode('utf-8')
        except:
            html = res.decode('gbk')
        if DEBUG:print(html)
        if html.find('bonjour') != -1:
            print('%s Seccess'%username)
            return True
        else:
            print('%s Failed'%username)
            #print(html)
            return False
    else:
        temp = _CURRENT_USER
        load_cookie(username)
        temp_b = test_cookie(username)
        load_cookie(temp)
        return temp_b
def delete_cookie(username):
    path = _COOKIE_PATH + "cookie_%s" % username
    if os.path.exists(path):
        os.remove(path)
    global  _CURRENT_USER
    if username ==  _CURRENT_USER:
        _CURRENT_USER = None
def login(username, password, save_cj=False):
    init()
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?\
entry=weibo&callback=sinaSSOController.preloginCallBack&rsakt=mod&\
checkpin=1&client=ssologin.js(v1.4.15)&_=%s' % str(int(time.time()))
    html = urlopen(prelogin_url).read().decode(_CHARSET)
    content = eval(html[html.find('(') + 1:html.find(')')])
    nonce = content['nonce']
    pubkey = content['pubkey']
    rsakv = content['rsakv']
    servertime = content['servertime']
    
    su = base64.b64encode(bytes(request.quote(username) , encoding='utf-8'))
    rsaPublickey = int(pubkey , 16)
    key = rsa.PublicKey(rsaPublickey , 65537)
    message = bytes(str(servertime) + '\t' + str(nonce) + '\n' + password , encoding='utf-8')
    sp = binascii.b2a_hex(rsa.encrypt(message , key))    

    post_data = {'entry' : 'weibo' , 'gateway' : 1 , 'from' : '' , 'savestate' : 7 , 'useticket' : 1 ,
                 'pagerefer' : 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D' ,
                 'vsnf' : 1 , 'su' : su , 'service' : 'miniblog' , 'servertime' : servertime ,
                 'nonce' : nonce , 'pwencode' : 'rsa2' , 'rsakv' : rsakv , 'sp' : sp ,
                 'sr' : '1680*1050' , 'encoding' : 'UTF-8' , 'prelt' : 961 ,
                 'url' : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'}

    html = urlopen('http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)' , post_data).read().decode('gb2312')
    if DEBUG:print(html)
    try:
        url = re.search("location.replace\('(.*?)'\);", html).group(1)
    except:
        url = re.search('location.replace\("(.*?)"\);', html).group(1)
    urlopen(url).read()
    global _CURRENT_USER
    _CURRENT_USER = username
    if not test_cookie(_CURRENT_USER):
        _CURRENT_USER = None
        raise Exception('Sina login failed!')
    elif save_cj:
        save_cookie(username)
def auto_login(username=None, save_cj=True):
    if not username:
        username_list =  list(_DEFAULT_USER.keys())
        cookie_list = [item[7:] for item in os.listdir(_COOKIE_PATH) if re.match('cookie_.+', item)]            
    else:
        username_list = [username]
        if os.path.exists(_COOKIE_PATH+'cookie_%s'%username):
            cookie_list = [username]
        else:
            cookie_list = []
    for cookie in cookie_list:
        time_login = get_login_time(cookie)
        if time_login:
            time_now = int(time.time())
            if time_now - time_login < _TIME_INTERVAL:
                load_cookie(cookie)
                if test_cookie(_CURRENT_USER):
                    return
                else:
                    delete_cookie(cookie)
    while username_list:
        username = username_list[0]
        if username in _DEFAULT_USER.keys():
            try:
                login(username, _DEFAULT_USER[username] , save_cj)
                return
            except:
                if len(username_list) > 1:
                    pass
                else:
                    raise Exception("couldn't auto-login")
        else:
            raise Exception("%s couldn't auto-login"%username)
        username_list.remove(username)
def login_all_default_user():
    name_bk = None
    for name in _DEFAULT_USER:
        print(name+' login...')
        try:
            login(name, _DEFAULT_USER[name], True)
            name_bk = name
        except:
            if DEBUG:raise
            delete_cookie(name)
            if name_bk:
                load_cookie(name_bk)
def change_user(username=None):
    if not _CURRENT_USER:
        raise Exception('not login yet')
    if not username:
        list_ = sorted([item[7:] for item in os.listdir(_COOKIE_PATH) if re.match('cookie_.+', item)])
        current_index = list_.index(_CURRENT_USER)
        if current_index + 1 >= len(list_):
            current_index = -1
        username = list_[current_index+1]
    load_cookie(username)
if __name__ == '__main__':
    login_all_default_user()