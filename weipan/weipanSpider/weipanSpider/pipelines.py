# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeipanspiderPipeline(object):
    def process_item(self, item, spider):
        return item


import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
import os
from weipanSpider.helpers.Mymongo import Mymongo
import hashlib

class MyFilesPipeline(FilesPipeline):
    '''
    继承框架自带的FilesPipeline文件下载类
    '''

    def get_media_requests(self, item, info):
        '''
        重写此方法， 用来获取图片url进行下载
        :param item:
        :param info:
        :return:
        '''
        print(item['fileurl'])
        mongo = Mymongo.get_instance()
        data = dict(item)
        data['md'] = hashlib.md5(data['fileurl'].encode(encoding = 'utf8')).hexdigest()
        self.table = mongo.table
        mongo.table.insert(data)
        yield scrapy.Request(item['fileurl'])

    def item_completed(self, results, item, info):
        '''
        下载完成后将会把结果送到这个方法
        :param results:
        :param item:
        :param info:
        :return:
        '''
        md = hashlib.md5(item['fileurl'].encode(encoding = 'utf8')).hexdigest()
        self.table.update({'md':md}, {"$set":{"result": results[0][0]}})
        print(results, 'xiazaiwancheng')

    def file_path(self, request, response=None, info=None):
        '''
        重写要保存的文件路径，不使用框架自带的hash文件名
        :param request:
        :param response:
        :param info:
        :return:
        '''
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('FilesPipeline.file_key(url) method is deprecated, please use '
                          'file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url
        md = hashlib.md5(url.encode(encoding = 'utf8')).hexdigest()
        temp = self.table.find_one({"md": md})
        if temp:
            return '%s%s' % (temp['path'], temp['filename'])

        return super().file_path(request, response, info)
