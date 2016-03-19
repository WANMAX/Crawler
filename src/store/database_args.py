'''
Created on 2016年1月19日

@author: wan
'''
import pymysql
from util import INSCHOOL
if INSCHOOL:
    HOST = '192.168.235.36'
    POST = 3306
else:
    HOST = '904939e.nat123.net'
    POST = 52335
USERNAME = 'fig'
PASSWORD = 'fig'
DATABASE = 'fig'
CHARSET = 'utf8'

try_ = 3
def get_conn():
    global try_
    while True:
        try:
            conn = pymysql.connect(host=HOST, user=USERNAME, passwd=PASSWORD, db=DATABASE, port=POST, charset=CHARSET)
            try_ = 3
            return conn
        except:
            try_ -= 1
            if not try_:
                raise