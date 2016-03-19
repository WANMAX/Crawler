'''
Created on 2015年11月17日

@author: wan
'''

import time

class Counter:
    def __init__(self, logger, num = 1, sleep=0):
        self.times = 0
        if num < 1 or type(num) != int:
            num = 1
        self.temp = self.cardinal_number = num
        self.logger = logger
        self.sleep = sleep
    def count(self):
        self.temp -= 1
        if self.temp <= 0:
            if self.sleep:
                time.sleep(self.sleep)
            self.times+=1
            self.logger.info('%u * %u = %u'%(self.times, self.cardinal_number, self.cardinal_number*self.times))
            self.temp = self.cardinal_number