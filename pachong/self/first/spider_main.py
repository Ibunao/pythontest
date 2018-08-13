# coding:utf-8

import html_downloader, html_parser, html_outputer, url_manager
import time
class SpiderMain():
    def __init__(self):
        # url管理器
        self.urls = url_manager.UrlManager()
        # 下载器
        self.download = html_downloader.HtmlDownloader()
        # 解析器
        self.parser = html_parser.HtmlParser()
        # 输出
        self.outputer = html_outputer.HtmlOutPuter()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while True:
            # try:
            new_url = self.urls.get_new_url()
            print('craw %d : %s' % (count, new_url))
            html_con = self.download.download(new_url)
            resp = self.parser.parse(new_url, html_con)
            if isinstance(resp, tuple):
                new_urls, new_data = resp
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
            else:
                self.urls.add_new_urls(resp)
            if count == 100000:
                break
            count = count + 1
            # except Exception as result:
            #     print(result)
            #     print('craw failed')
        self.outputer.output_html()


if __name__ == "__main__":
    start = time.time()

    root_url = "http://www.cnblogs.com/wupeiqi/articles/6000000.html"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)

    end = time.time()
    print('Running time: %s Seconds' % (end - start))
    fout = open('runingtime.md', 'w')

    fout.write('Running time: %s Seconds' % (end - start))
    fout.close()
