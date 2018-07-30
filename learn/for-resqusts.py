import requests
import json

def get():
    '''无参数get请求'''
    # # 发送请求
    # ret = requests.get('https://github.com/timeline.json')
    # # 请求的url
    # print(ret.url)
    # # 请求返回数据
    # print(ret.text)

    '''带参数请求'''
    # 设置请求参数
    params = {'key1': 'value1', 'key2': 'value2'}
    # 发送请求
    ret = requests.get('https://github.com/timeline.json', params=params)
    # 请求的url  https://github.com/timeline.json?key1=value1&key2=value2
    print(ret.url)
    # 请求返回数据
    print(ret.text)

# get()

def post():
    '''模拟表单请求'''
    # 设置请求参数
    params = {'key1': 'value1', 'key2': 'value2'}
    print(type(json.dumps(params)))
    # 发送请求
    ret = requests.post('http://temp.wuxingxiangsheng.com/test/request', data=params)
    # 请求的url
    print(ret.url)
    # 请求返回数据
    print(ret.text)
    # 返回cookie
    print(type(ret.cookies))
    print(ret.cookies)

    '''发送获取到的cookie'''
    # 发送请求
    ret = requests.post('http://temp.wuxingxiangsheng.com/test/request', data=params, cookies=ret.cookies)
    # 请求返回数据
    print(ret.text)
    print(ret.status_code)

# post()

# 解析
from bs4 import BeautifulSoup

def parse():
    # ret = requests.get('https://www.bunao.win/')
    # # 请求返回数据
    # print(ret.text)
    # soup = BeautifulSoup(ret.text, features="lxml")

    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
        <a href='abc.com'>bunao</a>
    </body>
    </html>
    """
    soup = BeautifulSoup(html_doc, features="lxml")
    # 查找第一个a标签
    tag = soup.find('a')
    print(tag)
    # 获取标签名
    name = tag.name
    print(name)
    # 获取标签属性
    attrs = tag.attrs
    print(attrs)
    # 设置标签属性
    tag.attrs = {'id': 123}
    tag.attrs['name'] = 'abc'
    # 重新设置标签名
    tag.name = 'span'
    print(soup)
    # 获取所有的子元素
    child = tag.children
    print(','.join(child))

parse()