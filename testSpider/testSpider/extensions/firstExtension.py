from scrapy import signals

class firstExtension(object):
    '''
    扩展类
    用来绑定scrapy内置的一些信号，当发出信号的时候执行绑定的方法
    '''
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_crawler(cls, crawler):
        '''
        会调用这个方法来创建此对象
        :param crawler:
        :return:
        '''
        # 获取配置数据
        val = crawler.settings.getint('MMMM')
        ext = cls(val)

        # 绑定信号的处理方法,更多信号查看 signals 类
        crawler.signals.connect(ext.my_def, signal = signals.spider_opened)

    def my_def(self):
        pass