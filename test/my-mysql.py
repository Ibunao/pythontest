#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql

class MMysql(object):
    '''
    非线程安全单利模式
    仿照yii 实现QueryBuild
    '''
    def __new__(cls, *args, **kwargs):
        '''
        实现单利
        '''
        if not hasattr(MMysql, '_instance'):
            MMysql._instance = object.__new__(cls)
            '''
            创建连接
            '''
            host, user, password, db = [*args]
            connect = pymysql.connect(host, user, password, db)
            MMysql.cursor = connect.cursor()
        return MMysql._instance
    def __init__(self, host, user, password, db):
        pass
    def from(self, table):
        pass
    def find(self):
        pass
    def update(self):
        pass
    def save(self):
        pass


test = MMysql('localhost', 'root', '123456', 'test')

def test(test):

