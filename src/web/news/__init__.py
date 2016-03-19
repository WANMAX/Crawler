from util.urlopen_and_read import urlopen_and_read
import logging
import gzip
    
_NEWS_MODULE_PATH = 'web.news.%s'
_RETRY_TIME = 1
_TRY_TIME = 3

BY_PAGE = True
BY_LAST_ID = False

def crawl_comments(module, todo, store_args, args):
    logger = logging.getLogger('crawlerLog')
    retry = _RETRY_TIME
    try_ = _TRY_TIME
    if module.TYPE:
        page = 1
    else:
        id = None
    while True:
        if module.TYPE:
            url = module.get_comment_page_url(page, args)
        else:
            url = module.get_comment_page_url(id, args)
        try:
            if type(url) == tuple:
                url, data = url
                html = urlopen_and_read(url, data).decode(module.COMMENT_CHARSET, 'ignore')
            else:
                html = urlopen_and_read(url).decode(module.COMMENT_CHARSET, 'ignore')
            if retry != _RETRY_TIME:
                retry = _RETRY_TIME
            if try_ != _TRY_TIME and module.TYPE:
                try_ = _TRY_TIME
        except:
            if retry:
                retry -=1
                continue
            logger.error("'%s' was not accessible"%url)
            if module.TYPE and try_:
                try_ -= 1
                page += 1
                continue
            else:
                logger.error("'%s' was not accessible and it's not the first failure"%url)
                break
        try:
            data = module.get_comment_source_list(html)
        except:
            break
        if not data:
            break
        list_ = []
        for comment_source in data:
            list_.append(comment_source)
        if not list:
            if module.TYPE and try_:
                try_ -= 1
                page += 1
                continue
            else:
                logger.error("The data from '%s' couldn't be found and it's not the first failure"%url)
                break
        elif module.TYPE:
            try_ = _TRY_TIME
        todo(list_, store_args)
        if module.TYPE:
            page += 1
        else:
            has_next = module.has_next(html)
            if not has_next:
                break
            id = module.get_next_id(html)