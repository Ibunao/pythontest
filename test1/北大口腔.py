import requests
import execjs
import json
import urllib
# r = requests.get('https://open.zwjk.com/appointment/zjyyAAA?phID=16')



def get_des_psswd(data):
    jsstr = get_js()
    ctx = execjs.compile(jsstr) #加载JS文件
    return (ctx.call('getHeaderInfo', json.dumps(data)))  #调用js方法  第一个参数是JS的方法名，后面的data是js方法的参数

def get_js():
    f = open("./beida.js", 'r', encoding='utf-8') # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr+line
        line = f.readline()
    return htmlstr


if __name__ == '__main__':
    # post请求时需要data参数
    data = {
        "url": 'https://open.zwjk.com/export/ui/patientVisits/rule?ucUiFlowId=98db3dd2-b2d2-11e6-a249-525400644ee2&scyUserId=95932a0f-b4d5-4daa-9fd5-04fb26dd1f45',
        "type": 'POST',
        "data" : ''
    }
    print(get_des_psswd(data))