'''
Created on 2016年1月22日

@author: wan
'''
import __init__
from store.database_args import get_conn

def work():
    conn = get_conn()
    cur = conn.cursor()
    sql = "select news_id, news_author from news where news_author != ''"
    cur.execute(sql)
    sql_pat = "update news set news_author = Null and news_image = '%s' where news_id = %u"
    for item in cur.fetchall():
        cur.execute(sql_pat%(item[1], item[0]))
        conn.commit()
        print(item)
    cur.close()
    conn.close()
if __name__ == '__main__':
    work()