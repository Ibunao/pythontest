# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from weipanSpider.items import WeipanspiderItem

class WeipanSpider(scrapy.Spider):
    name = 'weipan'
    # 这个不会过滤首页
    allowed_domains = ['weibo.com']
    # start_urls = ['http://vdisk.weibo.com/u/1358179637']

    def start_requests(self):
        # cookiejar 参数用来自动管理cookie， 可以自动管理多个，根据cookiejar对应的值不同
        return [Request('http://vdisk.weibo.com/u/1358179637', meta = {'cookiejar':1})]
    def parse(self, response):
        # 获取响应体
        # print(response.body)
        hrefs = response.xpath('//*[@id="share_table"]/tbody/tr/td[1]/div/div[2]/div/a/@href').extract()
        # print(pages)
        for href in hrefs:
            yield Request(href, meta = {'cookiejar':response.meta['cookiejar']}, callback=self.next)

    def next(self, response):
        path = response.xpath('//*[@id="sss"]/div[2]').extract_first()
        items = response.xpath('//tr/td[2]/div/div[2]/div/a')
        for item in items:
            # fileurl = item.xpath('@href').extract_first()
            # filename = item.xpath('@title').extract_first()
            # print(item, fileurl)
            # print(filename)
            # return
            filename = item.xpath('@title').extract_first()
            fileurl = item.xpath('@href').extract_first()
            # print(type(filename))
            # return
            if filename.find('.') == -1:
                yield Request(fileurl, meta = {'cookiejar':response.meta['cookiejar']}, callback=self.next)
                continue

            witem = WeipanspiderItem(path = path, fileurl = fileurl, filename = filename)
            yield witem
