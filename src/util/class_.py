'''
Created on 2015年11月7日

@author: wan
'''
from store.file_args import time_to_str
class News:
    def __init__(self, url, comment_url_args, title, content, source, date, source_url=None, author=None, abstract=None, news_image=None):
        self.url, self.comment_url_args, self.title, self.content, self.source, self.date, self.source_url, self.author, self.abstract, self.news_image = url, comment_url_args, title, content, source, date, source_url, author, abstract, news_image
    def __str__(self):
        extend = ''
        if self.source_url:
            extend += '<source_url>%s</source_url>\n'%self.source_url
        if self.author:
            extend += '<author>%s</author>\n'%self.author
        if self.news_image:
            extend += '<news_image>%s</news_image>\n'%self.news_image
        return '<news>\n<url>%s</url>\n<comment_url_args>%s</comment_url_args>\n<title>%s</title>\n<content>%s</content>\n<source>%s</source>\n<date>%s</date>\n%s</news>' % (self.url, str(self.comment_url_args), self.title, self.content, self.source, time_to_str(self.date), extend)
class Comment:
    def __init__(self, user_id, content, time, location=None, vote=None):
        self.user_id, self.content, self.time, self.location, self.vote = user_id, content, time, location, vote
    def __str__(self):
        extend = ''
        if self.location:
            extend += '<location>%s</location>'%self.location
        if self.vote:
            extend += '<vote>%u</vote>'%self.vote
        return '<comment><user_id>%s</user_id><content>%s</content><time>%s</time>%s</comment>' % (self.user_id, self.content, time_to_str(self.time), extend)
class Weibo:
    def __init__(self, mid, uid, content, time,
                 report_count, comment_count, zan_count, forward_uid=None, forward_content=None):
        (self.mid, self.uid, self.content, self.time, self.repost_count
         , self.comment_count, self.zan_count, self.forward_uid, self.forward_content)\
 = mid, uid, content, time, report_count, comment_count, zan_count, forward_uid, forward_content
    def __str__(self):
        if self.forward_uid:
            return  "<weibo><mid>%s</mid><uid>%s</uid><content>%s</content><time>%s</time>\
<repost_count>%s</repost_count><comment_count>%s</comment_count><zan_count>%s</zan_count>\
<forward_uid>%s</forward_uid><forward_content>%s</forward_content></weibo>"\
 % (self.mid, self.uid, self.content, time_to_str(self.time), self.repost_count, self.comment_count
    , self.zan_count, self.forward_uid, self.forward_content)
        else:
            return "<weibo><mid>%s</mid><uid>%s</uid><content>%s</content><time>%s</time>\
<repost_count>%s</repost_count><comment_count>%s</comment_count><zan_count>%s</zan_count></weibo>"\
 % (self.mid, self.uid, self.content, time_to_str(self.time), self.repost_count, self.comment_count, self.zan_count)
class WEIBO_COMMENT:
    def __init__(self, id, user_id, content, time):
        self.id, self.user_id, self.content, self.time = id, user_id, content, time
    def __str__(self):
        return '<comment><id></id><user_id>%s</user_id><content>%s</content><time>%s</time></comment>'\
             % (self.id, self.user_id, self.content, time_to_str(self.time))
class Repost:
    def __init__(self, id, user_id, content, time):
        self.id, self.user_id, self.content, self.time = id, user_id, content, time
    def __str__(self):
        return '<repost><id></id><user_id>%s</user_id><content>%s</content><time>%s</time></repost>'\
             % (self.id, self.user_id, self.content, time_to_str(self.time))
class Topic:
    def __init__(self, topic_name, topic_datetime, topic_type, topic_introduction, topic_args):
        self.topic_name, self.topic_datetime, self.topic_type, self.topic_introduction, self.topic_args = topic_name, topic_datetime, topic_type, topic_introduction, topic_args
    def __str__(self):
        return '<topic><topic_name>%s</topic_name><topic_datetime>%s</topic_datetime><topic_type>%s</topic_type><topic_introduction>%s</topic_introduction><topic_args>%s</topic_args></topic>'\
            %(self.topic_name, time_to_str(self.topic_datetime), self.topic_type, self.topic_introduction, str(self.topic_args))