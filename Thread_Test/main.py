#! /usr/bin/env python2.7
#coding=utf-8

import threading

class Swim(threading.Thread):
    def __init__(self,lock,people_name):
        super(Swim,self).__init__(name='Swim')#super()的使用是应对父类变化而设置的super(Swim,self) == threading.Thread
        self.lock = lock
        self.name = people_name
    def run(self):
        self.lock.acquire()
        print str(self.name)
        self.lock.release()

lock = threading.Lock()
Swim(lock,'song').start()
Swim(lock,'wu').start()

