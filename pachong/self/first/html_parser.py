import re

from bs4 import BeautifulSoup
'''解析'''
class HtmlParser(object):
    def parse(self, new_url, html_con):
        if new_url is None or html_con is None:
            return
        soup = BeautifulSoup(html_con,'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(new_url, soup)
        new_data = self._get_new_data(new_url, soup)
        return new_urls,new_data

    def _get_new_data(self, page_url, soup):
        res_data = {}

        # url
        res_data['url'] = page_url

        title_node = soup.find('a', id="cb_post_title_url")
        res_data['title'] = title_node.get_text()

        return res_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        base = page_url[:-12]
        num = page_url[-12:-5]
        suffix = page_url[-5:]
        print(type(int(num)))

        new_num = int(num) + 1
        new_url = base + str(new_num) + suffix
        new_urls.add(new_url)
        return new_urls


