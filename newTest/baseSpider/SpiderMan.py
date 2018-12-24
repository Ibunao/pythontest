#!/usr/bin/env python3
# -*-coding:utf-8-*-
import DataOutput
import HtmlDownloader
import HtmlPaser
import UrlManager

class SpiderMan(object):
    '''
    爬虫调度器
    '''
    def __init__(self):
        self.output = DataOutput
        self.downloader = HtmlDownloader
        self.paser = HtmlPaser
        self.manager = UrlManager

    def crawl(self, root_url):
        # 添加入口URL
        self.manager.add_new_url(root_url)
        # 判断url管理器中是否有新的url，同时判断抓了多少个URL
        while(self.manager.has_new_url() and self.manager.old_url_size() < 100):
            try:
                # 从url管理器获取新的url
                new_url = self.manager.get_new_url()
                # html下载器下载网页
                html = self.downloader.download(new_url)
                # html解析器抽取网页数据
                new_urls, data = self.paser.parser(new_url, html)
                # 将抽取的url添加到url管理器中
                self.manager.add_new_urls(new_urls)
                # 数据存储器存储数据
                self.output.store_data(data)
                print('已经抓取 %s 个链接'%self.manager.old_url_size())
            except Exception:
                print('出现异常')
        # 输出数据
        self.output.output_html()

if __name__ == "__main__":
    spider = SpiderMan()
    spider.crawl('https://www.bunao.win')
