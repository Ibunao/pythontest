#coding=utf-8
import requests
from lxml import etree
from pymongo import MongoClient
import time

class Qiubai_spider():
    def __init__(self):
        self.url = "http://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"
        }
        # 连接mongo
        self.client = MongoClient('118.25.38.240', 27017)
        # 选择使用的数据库
        db_auth = self.client['spider_test']
        # 验证登陆
        db_auth.authenticate("spider", "spider123")
        self.db = self.client['spider_test']

    def parse_url(self, url):
        response = requests.get(url, timeout=10, headers=self.headers) #请求url
        if response.status_code != 200 :
            raise Exception('响应码错误 %s 响应码 %s' % (url, response.status_code))  #当响应码不是200时候，做断言报错处理
        print(url)
        return etree.HTML(response.text) #返回etree之后的html

    def parse_content(self,html):
        item_temp = html.xpath('//div[@class="content"]')
        print(len(item_temp))
        for item in item_temp:
            content = item.xpath("./span/text()")[0].replace("\n", "") #获取内容
            # 向集合中添加数据
            self.db['xiushibaike'].insert({'content': content})
            print(content)


    def run(self):
        '''函数的主要逻辑实现
        '''
        i = 10
        while i <= 30 :
            url = self.url.format(i) #获取到url
            html = self.parse_url(url) #请求url
            self.parse_content(html) #解析页面内容并把内容存入内容队列
            i += 1
            time.sleep(1)

        self.client.close()

if __name__ == "__main__":
    qiubai = Qiubai_spider()
    qiubai.run()