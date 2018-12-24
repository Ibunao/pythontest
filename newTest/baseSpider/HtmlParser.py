#!/usr/bin/env python3
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup
class HtmlPaser(object):
    '''
    html解析器
    '''
    def parser(self, page_url, html_cont):
        '''
        解析网页内容，抽取url和数据
        :param page_url: 下载页面的url
        :param html_cont: 下载页面的内容
        :return:
        '''
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding= 'utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
    def _get_new_url(self, page_url, soup):
        '''
        从解析器中获取新的url集合
        :param page_url: 下载的URL，页面中有的是相对位置，可能会用到
        :param soup: 解析器
        :return:
        '''
        new_urls = set()

        # 解析的逻辑

        return new_urls
    def _get_new_data(self, page_url, soup):
        '''
        从解析器获取需要的数据
        :param page_url: 下载的url
        :param soup: 解析器
        :return:
        '''
        data = {}
        data['url'] = page_url

        # 解析的逻辑

        return data