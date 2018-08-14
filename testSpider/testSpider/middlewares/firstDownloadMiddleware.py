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
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
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
        spider.logger.info('Spider opened: %s' % spider.name)