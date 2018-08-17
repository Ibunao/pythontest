import requests

proxies = {'http': 'http://121.235.202.194:65309'}
url = 'http://temp.wuxingxiangsheng.com/test/request'
resp = requests.get(url, proxies=proxies)
print(resp)