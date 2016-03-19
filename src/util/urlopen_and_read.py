'''
Created on 2016年1月13日

@author: wan
'''
from util import PROXY
from urllib.error import HTTPError
if PROXY:
    try:
        from tool.proxy import urlopen
    except:
        from urllib.request import urlopen
else:
    from urllib.request import urlopen
import socket
import gzip
import urllib.request
import urllib.parse
_HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
            'Accept-Encoding':'gzip'}  
_CHARSET = 'utf-8'

    
def urlopen_and_read(fullurl, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    try:
        if data:
            data = urllib.parse.urlencode(data).encode(_CHARSET)
        req = urllib.request.Request(fullurl, data, _HEADERS)  
        resp = urlopen(req, timeout=timeout)
    except HTTPError as e:
        resp = e
    result = resp.read()
    if resp.info().get('Content-Encoding') == 'gzip':
        result = gzip.decompress(result)
    return result