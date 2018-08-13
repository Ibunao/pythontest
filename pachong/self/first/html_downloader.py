import requests

'''下载器'''
class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None

        response = requests.get(url)
        if response.status_code != 200:
            return None
        res = response.text
        return res