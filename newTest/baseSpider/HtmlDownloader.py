#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
class HtmlDownloader(object):
    '''
    html下载器
    '''
    def download(self, url):
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        headers = {'User-Agent': user_agent}
        r =requests.get(url, headers = headers)
        if r.status_code == 200:
            return r.content.decode()
        return None