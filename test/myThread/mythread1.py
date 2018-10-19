#coding=utf-8
import threading
import time

def saySorry():
    print('执行了')
    time.sleep(3)
    print("亲爱的，我错了，我能吃饭了吗？")

if __name__ == "__main__":
    for i in range(5):
        t = threading.Thread(target=saySorry)
        print('还没开始')
        t.start() #启动线程，即让线程开始执行
        print('结束了')
    print(len(threading.enumerate()))
    print('主线程要结束了')