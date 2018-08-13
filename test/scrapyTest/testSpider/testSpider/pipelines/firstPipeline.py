import json
from scrapy.exceptions import DropItem
class firstPipeline(object):
    def __init__(self):
        self.file = open('papers.json', 'wb')

    def process_item(self, item, spider):
        # print(item['img'])
        if item['img']:
            line = json.dumps(dict(item)) + '\n'
            # 要转成字节类型
            self.file.write(line.encode())
            return item
        else:
            raise DropItem('miss img in %s' % item)
