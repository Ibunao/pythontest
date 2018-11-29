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
        self.item = item
        print(item['fileurl'])
        yield scrapy.Request(item['fileurl'])

    def item_completed(self, results, item, info):
        '''
        下载完成后将会把结果送到这个方法
        :param results:
        :param item:
        :param info:
        :return:
        '''
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


        return '%s/%s' % (self.item.path, self.item.filename)