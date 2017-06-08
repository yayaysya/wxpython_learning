#! /usr/bin/env python2.7
#coding=utf-8

import threading

lock = threading.Lock()
def thread1():
    lock.acquire()
    count = 0
    for i in range(10):
        count += i
    print count

threading.Thread(target= thread1, args=(), name= 'thread1').start()
