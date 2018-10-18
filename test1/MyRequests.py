import requests

proxies = {'http': 'http://121.235.202.194:65309'}
url = 'http://temp.wuxingxiangsheng.com/test/request'
# resp = requests.get(url, proxies=proxies) # 携带代理
# resp = requests.get(url)
# print(resp.cookies)
# print(resp.text)
# resp = requests.get(url, cookies=resp.cookies)
# print(resp.text)


# url = 'https://www.coinegg.com/?lang=zh_CN?lang=zh_CN';
# resp = requests.get(url)
# print(resp.cookies)
# print(resp.text)


url = 'https://www.coinegg.com/coin/btc/allcoin?t=0.09733049332617782'
'''
accept: application/json, text/javascript, */*; q=0.01
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
cookie: __cfduid=d24b9f33c360b64a25f35082dc541d02a1535128516; lang=en_US; USER_PW=e06125c874633f24f82c52ca763db81d; PHPSESSID=87cf99e5da505af6a283726ef9f154e3; languageStyle=1; UM_distinctid=1656ccaa21c41a-095e32bb601ade-34677909-fa000-1656ccaa21d269; _ga=GA1.2.268555327.1535128545; _gid=GA1.2.1557074852.1535128545; __zlcmid=o3hag9VnJcG4G5; cf_clearance=3639ed4a331ac351739d4564fb6935e3d5bfbc16-1535186673-900-150; CNZZDATA1273484625=572760576-1535125728-https%253A%252F%252Fwww.coinegg.com%252F%7C1535182882; _gat_gtag_UA_108097775_1=1
pragma: no-cache
referer: https://www.coinegg.com/?lang=zh_CN?lang=zh_CN
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
x-requested-with: XMLHttpRequest
'''
headers = {
'accept': 'application/json, text/javascript, */*; q=0.01',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'no-cache',
'cookie': '__cfduid=d24b9f33c360b64a25f35082dc541d02a1535128516; lang=en_US; USER_PW=e06125c874633f24f82c52ca763db81d; PHPSESSID=87cf99e5da505af6a283726ef9f154e3; languageStyle=1; UM_distinctid=1656ccaa21c41a-095e32bb601ade-34677909-fa000-1656ccaa21d269; _ga=GA1.2.268555327.1535128545; _gid=GA1.2.1557074852.1535128545; __zlcmid=o3hag9VnJcG4G5; cf_clearance=3639ed4a331ac351739d4564fb6935e3d5bfbc16-1535186673-900-150; CNZZDATA1273484625=572760576-1535125728-https%253A%252F%252Fwww.coinegg.com%252F%7C1535182882; _gat_gtag_UA_108097775_1=1',
'pragma': 'no-cache',
'referer': 'https://www.coinegg.com/?lang=zh_CN?lang=zh_CN',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
'x-requested-with': 'XMLHttpRequest'
}
resp = requests.get(url, headers = headers)
print(resp.cookies)
print(resp.text)

