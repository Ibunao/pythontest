import scrapy
from scrapy.pipelines.images import ImagesPipeline

class MyImagesPipeline(ImagesPipeline):
    '''
    继承框架自带的ImagesPipeline图片下载类，可以下载的同时生成不同尺寸的图片放在配置的目录下
    '''

    def get_media_requests(self, item, info):
        '''
        重写此方法， 用来获取图片url进行下载
        :param item:
        :param info:
        :return:
        '''
        yield scrapy.Request(item['img'])

    def item_completed(self, results, item, info):
        '''
        下载完成后将会把结果送到这个方法
        :param results:
        :param item:
        :param info:
        :return:
        '''
        print(results)

        '''
        results 为下载返回的数据, 如下 
        [(True, {'url': 'https://img3.doubanio.com/view/subject/m/public/s29827942.jpg', 'path': 'full/ad6acfdbef4d9df208c0e010ed1efcc287cb6225.jpg', 'checksum': 'c5d853689829ba8731cbb27146d89573'})]
        图片下载成功时为True
        url 源图片地址
        path 下载的文件路径
        checksum md5 hash
        '''
        print(item)
        print(info)