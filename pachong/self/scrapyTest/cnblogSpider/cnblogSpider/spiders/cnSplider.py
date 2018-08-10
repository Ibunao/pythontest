# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request

class CnspliderSpider(scrapy.Spider):
    # 爬虫名
    name = 'cnSplider'
    # 允许的域名
    allowed_domains = ['linkeddb.com']
    # 开始的url
    start_urls = ['https://www.linkeddb.com/']

    def parse(self, response):
        # print(response.url)
        selector = Selector(response = response)
        hxs = selector.xpath('//a')
        print(hxs)
