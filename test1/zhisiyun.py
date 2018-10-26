import requests
import json

def post():
    '''模拟表单请求'''
    # 设置请求参数
    params = {'userid': '597550941f62939e2913bb43'}
    print(type(json.dumps(params)))
    # 发送请求
    ret = requests.post('https://www.zhisiyun.com/wxapp/login_user', data=params)
    # 请求的url
    print(ret.url)
    # 请求返回数据
    print(ret.text)
    # 返回cookie
    print(type(ret.cookies))
    print(ret.cookies)

    '''发送获取到的cookie'''
    params = {'position' : '嘉定总部',
			'longitude' : 121.20988,
			"latitude" : 31.408887,
			"distance" : 67.59726443498181}
    # 发送请求
    ret = requests.post('https://www.zhisiyun.com/admin/clock_method/clockInOut', data=params, cookies=ret.cookies)
    # 请求返回数据
    print(ret.text)
    print(ret.status_code)
post()