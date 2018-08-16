import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
import os

class MyFilesPipeline(FilesPipeline):
    '''
    继承框架自带的FilesPipeline文件下载类
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
        # print(results)

        '''
        results 为下载返回的数据, 如下 
        [(True, {'url': 'https://img3.doubanio.com/view/subject/m/public/s29816983.jpg', 'path': 'full/fced9acc2ecf23e0f96b9a2d9a442b02234f4388.jpg', 'checksum': 'ce0e7d543b37dbe3d21dd46ef8fcbd1b'})]
        图片下载成功时为True
        url 源图片地址
        path 下载的文件路径
        checksum md5 hash
        '''
        print(item)
        print(info)

    def file_path(self, request, response=None, info=None):
        '''
        重写要保存的文件路径，不使用框架自带的hash文件名
        :param request:
        :param response:
        :param info:
        :return:
        '''
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('FilesPipeline.file_key(url) method is deprecated, please use '
                          'file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # 后缀
        media_ext = os.path.splitext(url)[1]  # change to request.url after deprecation
        return 'full/%s%s' % (media_guid, media_ext)