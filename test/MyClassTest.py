#!/usr/bin/env python
# -*- coding:utf-8 -*-

class MyDing(object):
    count = 0;
    def __new__(cls, *args, **kwargs):
        print('new',*args, kwargs)
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print('init',args, kwargs)
    def ran(self):
        print('ran')
    @staticmethod
    def bunao():
        MyDing.myClassmethod()
        print('bunao')

    @classmethod
    def myClassmethod(cls):
        cls.count += 1
        print('myClassmethod',cls)

class MyMyClass(MyDing):
    pass

ran = {"gggggg":"ran"}
aaa = (1,2,3)
# bunao = MyDing(*aaa, **ran)
# bunao.ran()
# bunao.myClassmethod()
# bunao.bunao()

# MyDing.myClassmethod()
# MyDing.bunao()
# print(bunao.count)

bunao = MyMyClass(*aaa, **ran)
bunao.ran()
bunao.myClassmethod()
bunao.bunao()