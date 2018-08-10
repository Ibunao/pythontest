# -*- coding: utf-8 -*-
import scrapy
from ..items import BigfileItem


class ChoutiSpider(scrapy.Spider):
    name = "chouti"
    allowed_domains = ["chouti.com"]
    start_urls = (
        'http://www.chouti.com/',
    )

    def parse(self, response):
        yield BigfileItem(url='https://wx1.sinaimg.cn/large/8a04ef95ly1frbvy0d2opj20j00tm0vt.jpg',type='file',file_name='xx.jpg')
