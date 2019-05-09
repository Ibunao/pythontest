from pynput.keyboard import Listener
import os
import logging
import requests
import time

path = "D:\\keyword-py\\"
if(not os.path.exists(path)):
    os.mkdir(path)

logging.basicConfig(filename=(path + "keylogger.txt"), format="%(asctime)s:%(message)s", level=logging.DEBUG)

str = ''
starttime = 0
endtime = 0
maxScanTime = 300
# 毫秒级时间戳
nowTime = lambda:int(round(time.time() * 1000))
from playsound import playsound
# temp = requests.get('http://www.baidu.com')
# print(temp.text)
def press(key):
    global str, starttime, endtime, maxScanTime
    keyStr = ''
    # print(key.__dict__)

    if not starttime:
        starttime = nowTime()
    # 获取键盘输入的值
    if hasattr(key, 'name'):
        keyStr = key.name

    # 复杂的可能还要判断delete和backspace删除键

    # 如果是字符则记录
    else:
        if hasattr(key, 'char'):
            keyStr = key.char

    print(starttime)
    # 如果按的是enter键
    if (keyStr == 'enter'):
        endtime = nowTime()
        logging.info(str)
        # 如果是数值类型 时间间隔符合扫描抢
        if str.isdigit() and endtime - starttime < maxScanTime:
            print(str)
            url = 'http://128.128.1.125:8888/queryProBox?barcode='.str
            # 播放mp3
            playsound('auido.mp3')
        str = ''
        starttime = 0
    # 不是enter键，则拼接
    else:
        str = str + keyStr


with Listener(on_press=press) as listener:
    listener.join()