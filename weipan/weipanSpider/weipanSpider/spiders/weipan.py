# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request

class WeipanSpider(scrapy.Spider):
    name = 'weipan'
    # 这个不会过滤首页
    allowed_domains = ['weibo.com']
    # start_urls = ['http://vdisk.weibo.com/u/1358179637']
    # 测试请求参数的连接
    start_urls = []

    def start_requests(self):
        yield Request('http://temp.wuxingxiangsheng.com/test/request', meta={'cookiejar': 1})
    def parse(self, response):
        print(response.body)
        yield Request('http://temp.wuxingxiangsheng.com/test/request', meta={'cookiejar': 1})
        print(response.body)
        pass
