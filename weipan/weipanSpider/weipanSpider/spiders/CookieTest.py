# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request

class WeipanSpider(scrapy.Spider):
    name = 'test'
    # 这个不会过滤首页
    # allowed_domains = ['weibo.com']
    allowed_domains = ['wuxingxiangsheng.com']
    # start_urls = ['http://vdisk.weibo.com/u/1358179637']
    # 测试请求参数的连接
    start_urls = []

    def start_requests(self):
        # cookiejar 参数用来自动管理cookie， 可以自动管理多个，根据cookiejar对应的值不同
        return [Request('http://temp.wuxingxiangsheng.com/test/request', meta = {'cookiejar':1})]
    def parse(self, response):
        # 获取响应体
        print(response.body)
        # 获取响应的cookie
        print(response.headers.getlist('Set-Cookie'))
        # 获取cookiejar对应的值 1
        print(response.meta['cookiejar'])
        # cookies 为自定义cookie值  meta = {'cookiejar' 为自动管理的cookie
        yield Request('http://temp.wuxingxiangsheng.com/test/request?i=1', cookies={'test':'test'},
                      meta = {'cookiejar':response.meta['cookiejar']}, callback=self.next)

    def next(self, response):
        # 获取请求携带的cookie， 自定义的加自动管理的
        cookie = response.request.headers.getlist('Cookie')
        print('请求时携带请求的Cookies：', cookie)
        print(response.body)