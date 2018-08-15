from scrapy import signals


class firstDownloadMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        '''
        类方法用来创建中间件
        :param crawler:
        :return: 对象
        '''

    def process_request(self, request, spider):
        '''
        请求需要被下载时通过此方法
        当request通过下载中间件的时，该方法调用，用来处理请求，理解成请求过程
        参数：
        request:处理的请求对象
        spider: 该request对应的spider
        返回值：
        None：scrapy将继续处理该request，执行其他的中间件或下载器处理
        response对象：将不会往后走请求过程，而是直接开始执行相应过程，走中间件的process_response这条路
        request对象：停止往后走，重新调度这个request
        raise IgnoreRequest：抛出异常，中间件的process_exception()方法将会被调用，如果没有处理该异常的，则Request
        的errback方法会被调用，如果没有代码处理抛出的异常，该异常被忽略且不记录
        :param request:
        :param spider:
        :return:
        '''

        return None

    def process_response(self, request, response, spider):
        '''
        当response通过下载中间件的时候调用该方法，用来处理响应，理解成处理响应数据的过程
        :param request:
        :param response:
        :param spider:
        :return:
        '''
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        '''
        爬虫启动时调用
        :param spider:
        :return:
        '''
        spider.logger.info('Spider opened: %s' % spider.name)


import random
class RandomUserAgent(object):
    '''
    使用随机 User-Agent的中间件
    '''
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        '''
        通过这个类方法创建对象
        :param crawler:
        :return:
        '''
        '''
        settings.py USER_AGENTS的值示例
        USER_AGENT = [
            'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        ]

        '''
        # 获取配置文件settings中USER_AGENTS的值
        return cls(crawler.settings.getlist('USER_AGENTS'))


    def process_request(self, request, spider):
        '''
        中间件请求过程中设置request
        :param request:
        :param spider:
        :return:
        '''
        # 设置request的的User-Agent头
        request.headers.setdefault("User-Agent", random.choice(self.agents))


class RandomProxy(object):
    '''
    使用随机代理的中间件
    '''
    def __init__(self, iplist):
        self.iplist = iplist

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('IPLIST'))

    def process_request(self, request, spider):
        '''
        给代理随机添加上一个代理
        :param request:
        :param spider:
        :return:
        '''
        proxy = random.choice(self.iplist)
        request.meta['proxy'] = proxy
