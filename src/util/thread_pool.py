'''
Created on 2015年6月12日

@author: wan
'''

from threading import Thread
import time

NUM = 10
_threads = []
_runing_threads = []

def set_thread_num(num):
    global NUM
    NUM = num
def get_threads():
    return _threads
def join(time_=0):
    time.sleep(time_)
    while True:
        time.sleep(0.5)
        for thread in _runing_threads:
            if thread.isAlive():
                thread.join()
        if not _runing_threads:
            break

_generator = None
def set_generator(generator):
    global _generator
    _generator = generator
_tag = False
def _run():
    global _generator
    global _tag
    global _threads
    _tag = True
    while True:
        while  True:
            for thread in _runing_threads:
                if not thread.isAlive():
                    _runing_threads.remove(thread)
            if len(_runing_threads) < NUM:
                break;
            time.sleep(0.5)
        if not _generator:
            if not _threads:
                _tag = False
            else:
                thread = _threads[0]
        else:
            try:
                thread = next(_generator)
            except:
                _tag = False
        if not _tag:
            if _runing_threads:
                continue
            else:
                if _generator:
                    _generator = None
                break
        if not _generator:
            _threads.remove(thread)
        _runing_threads.append(thread)
        thread.start()
def start():
    if not _tag:
        Thread(target=_run).start()
def stop():
    global _tag
    _tag = False;
def add(method,args):
    global _threads
    _threads.append(Thread(target=_decorate_method(method),args = args))
def _decorate_method(method):
    def temp(*args):
        method(*args)
    return temp
