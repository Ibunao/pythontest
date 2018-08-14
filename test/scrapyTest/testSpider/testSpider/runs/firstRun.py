from ..spiders.firstSpider import FirstspiderSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

def my_run1():
    '''
    启动单个爬虫，这里可以定制爬虫的配置
    :return:
    '''
    process = CrawlerProcess(get_project_settings())
    process.crawl(FirstspiderSpider)
    process.start()

def my_run2():
    '''
    启动多个爬虫，这里可以给每个爬虫定制配置
    :return:
    '''
    process = CrawlerProcess(get_project_settings())
    process.crawl(FirstspiderSpider)
    process.crawl(FirstspiderSpider)
    process.start()

if __name__ == '__main__':
    my_run1()