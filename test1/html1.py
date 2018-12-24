#!/usr/bin/env python3
# -*-coding:utf-8-*-

import json
import requests
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import urllib

resp = requests.get('https://quanmin.baidu.com/feedvideoui/api/videotopic?cursor=1&tid=5341907154927488731&tabId=hot')
temp = resp.text
mydict = json.loads(temp)
tpl = mydict['data']['tpl']
# print(tpl)
# 构造response对象
response = HtmlResponse(url='', body=tpl, encoding='utf-8')
selector = Selector(response=response)
# 获取第一个
item = selector.xpath('//li/div/@data-cmd').extract_first()
# print(item)
str = urllib.parse.unquote(item)
print(str)