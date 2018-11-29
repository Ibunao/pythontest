# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from weipanSpider.items import WeipanspiderItem
import json
import re
import time

class WeipansearchSpider(scrapy.Spider):
    '''
    搜索功能微盘已经关闭，更改为资源链接进行搜索
    '''
    name = 'weipansearch'
    allowed_domains = ['weibo.com']
    target_url = 'http://vdisk.weibo.com/s/uHTIBIt1MzT7z?parents_ref=&category_id=&pn='
    get_down_info = 'http://vdisk.weibo.com/api/weipan/fileopsStatCount?link={link}&ops=download&wpSign={sign}&_={time}'
    page = 1
    def start_requests(self):
        # cookiejar 参数用来自动管理cookie， 可以自动管理多个，根据cookiejar对应的值不同
        return [Request(self.target_url+str(self.page), meta = {'cookiejar':1})]
    def parse(self, response):
        # 获取响应体
        # print(response.body)
        sign = re.search("var SIGN = \'(.+)\';", response.text).group(1)
        # print(sign)
        items = response.xpath('//tbody/tr')
        for item in items:
            info = item.xpath('.//th/span/a[1]/@data-info').extract_first()
            info = json.loads(info)
            # print(self.get_down_info.format(link=info['copy_ref'], sign=sign, time = int(round(time.time() * 1000))))
            href = self.get_down_info.format(link=info['copy_ref'], sign=sign, time = int(round(time.time() * 1000)))
            yield Request(href, meta={'cookiejar': response.meta['cookiejar']}, callback=self.next)

        # for href in hrefs:
        #     yield Request(href, meta = {'cookiejar':response.meta['cookiejar']}, callback=self.next)

    def next(self, response):
        # print(response.body)
        info = json.loads(response.text)
        print(info)
        witem = WeipanspiderItem(path = '', fileurl = info['url'], filename = info['title'])
        yield witem


