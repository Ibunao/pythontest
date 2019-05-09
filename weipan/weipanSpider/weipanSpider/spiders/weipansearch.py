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
    # 首页数据
    target_url = 'http://vdisk.weibo.com/u/1881788364?page='
    # 抓取的目标url
    # target_url = 'http://vdisk.weibo.com/s/uiPfBB4ijcB7?parents_ref=&category_id=&pn='
    # 子子目录
    # target_url = 'http://vdisk.weibo.com/s/uiPfBB4iBrNH?parents_ref=,uiPfBB4iBrNH&category_id=0&pn='
    # 基础路径，爬取不同的用户需要设置一下
    route = 'Bob_LSC'
    get_down_info = 'http://vdisk.weibo.com/api/weipan/fileopsStatCount?link={link}&ops=download&wpSign={sign}&_={time}'
    page = 1
    def start_requests(self):
        # cookiejar 参数用来自动管理cookie， 可以自动管理多个，根据cookiejar对应的值不同
        return [Request(self.target_url+str(self.page), meta = {'cookiejar':1, 'filepath':'/'})]
    def parse(self, response):

        # 获取响应体
        # print(response.body)
        # 获取 SIGN
        sign = re.search("var SIGN = \'(.+)\';", response.text).group(1)
        # print(sign)
        items = response.xpath('//tbody/tr')
        # print(items)
        # 如果下一页没有则不往下进行了，要结束了
        if not len(items):
            return

        for item in items:
            # info = item.xpath('.//th/span/a[1]/@data-info').extract_first()
            # 首页没分类的不是th
            info = item.xpath('.//td[2]/span/a[1]/@data-info').extract_first()
            print(info)
            info = json.loads(info)
            if info['is_dir']:
                # 文件夹的话还是手动下载吧
                # self.process_dir(info, response)
                # filepath = response.meta['filepath'] + info['filepath'] + '/'
                # print('wenjianjia:' + filepath)
                # yield Request(info['link'], meta={'cookiejar': response.meta['cookiejar'], 'filepath': filepath},
                #               callback=self.parse)
                continue
            # print(self.get_down_info.format(link=info['copy_ref'], sign=sign, time = int(round(time.time() * 1000))))
            href = self.get_down_info.format(link=info['copy_ref'], sign=sign, time = int(round(time.time() * 1000)))
            yield Request(href, meta={'cookiejar': response.meta['cookiejar'], 'filepath': response.meta['filepath']}, callback=self.next)

        # 看是否有下一页
        nextpage = response.xpath('//div[@class="vd_page"]/a[@class="vd_bt_v2 vd_page_btn"]/span["下一页"]/text()')
        print('jijiangxiayiye', nextpage, len(nextpage))
        if len(nextpage):
            print('haibulai')
            # self.my_process_next(response)
            self.page += 1
            print('dijiye' + str(self.page))
            yield Request(self.target_url + str(self.page),
                          meta={'cookiejar': response.meta['cookiejar'], 'filepath': response.meta['filepath']},
                          callback=self.parse)
    # 封装成方法后上面调用不到
    def my_process_next(self, response):
        print('laile')
        self.page += 1
        print('dijiye'+ str(self.page))
        yield Request(self.target_url+str(self.page), meta={'cookiejar': response.meta['cookiejar'], 'filepath': response.meta['filepath']}, callback=self.parse)

    # 封装成方法后上面调用不到
    def process_dir(self, info, response):
        filepath = response.meta['filepath']+info['filepath']+'/'
        print('wenjianjia:'+filepath)
        yield Request(info['link'], meta={'cookiejar': response.meta['cookiejar'], 'filepath': filepath}, callback=self.parse)

    def next(self, response):
        # print(response.body)
        info = json.loads(response.text)
        print(info, response.meta['filepath'])
        witem = WeipanspiderItem(path = self.route+response.meta['filepath'], fileurl = info['url'], filename = info['title'])
        yield witem


