# -*- coding: utf-8 -*-
import scrapy
from ..items.firstspiderItem import firstspiderItem

class FirstspiderSpider(scrapy.Spider):
    # 爬虫名，必填
    name = 'firstSpider'
    # 允许访问的域名
    allowed_domains = ['douban.com']
    # 开始的url
    start_urls = ['https://book.douban.com/']

    def parse(self, response):
        '''
        解析
        :param response:
        :return:
        '''
        papers = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[2]/div/div/ul[2]/li')
        # print(papers)
        for paper in papers:
            url = paper.xpath('.//div/a/@href').extract_first()
            img = paper.xpath('.//div/a/img/@src').extract_first()
            content = paper.xpath('.//div/div/a/text()').extract_first()
            # print(url, img, content)
            item = firstspiderItem(url = url, img = img, content = content)
            yield item
        # 分析下一个请求
