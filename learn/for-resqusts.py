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
    ret = requests.get('https://www.bunao.win/')
    # 请求返回数据
    print(ret.text)
    soup = BeautifulSoup(ret.text, features="lxml")
    soup.find('header')

parse()