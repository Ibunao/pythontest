#coding=utf-8
import requests
from lxml import etree
from pymongo import MongoClient
import time

class Qiubai_spider():
    def __init__(self):
        self.url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findKjxx/forIssue?name=ssq&code=2018131"
        self.headers = {
            "Referer":"http://www.cwl.gov.cn/kjxx/ssq/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
        # 连接mongo
        # self.client = MongoClient('118.25.38.240', 27017)
        # # 选择使用的数据库
        # db_auth = self.client['spider_test']
        # # 验证登陆
        # db_auth.authenticate("spider", "spider123")
        # self.db = self.client['spider_test']

    def parse_url(self, url):
        # response = requests.get("http://www.cwl.gov.cn/kjxx/ssq/", timeout=10, headers=self.headers)
        # time.sleep(3)
        response = requests.get(url, timeout=10, headers=self.headers) #请求url
        print(response, response.content)
        return
        if response.status_code != 200 :
            raise Exception('响应码错误 %s 响应码 %s' % (url, response.status_code))  #当响应码不是200时候，做断言报错处理
        print(url)
        return etree.HTML(response.text) #返回etree之后的html

    def parse_content(self,html):
        return
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

        self.parse_url(self.url)


        # self.client.close()

if __name__ == "__main__":
    qiubai = Qiubai_spider()
    qiubai.run()