
class firstSpiderMiddleware(object):
    '''
    spider中间件
    '''
    def process_spider_input(self, response, spider):
        '''
        下载完成，执行，然后交给parse处理
        当response通过spider中间件时，调用该方法，处理该response
        返回值和含义和下载中间件的对应相似，不重复解释了
        :param response:
        :param spider:
        :return:
        '''
        pass

    def process_spider_output(self, response, result, spider):
        '''
        当spider处理request返回result时调用，通往pipeline
        :param response:
        :param result:
        :param spider:
        :return:
        '''
        pass

    def process_spider_exception(self, response, exception, spider):
        '''
        接收异常
        :param response:
        :param exception:
        :param spider:
        :return:
        '''
        pass
    def process_start_requests(self, start_requests, spider):
        '''
        爬虫启动时调用
        :param start_requests:
        :param spider:
        :return:
        '''
        pass