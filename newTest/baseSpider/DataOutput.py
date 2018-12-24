#!/usr/bin/env python3
# -*-coding:utf-8-*-
class DataOutput(object):
    '''
    数据存储器
    '''

    def __init__(self):
        self.datas = []

    def store_data(self, data):
        '''
        保存数据
        :param data: 要存储的数据 {}
        :return:
        '''
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        '''
        将数据输出成html格式的
        :return:
        '''

        # 输出逻辑
