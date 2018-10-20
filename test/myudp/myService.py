#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket

def main():
    msg = '收到并返回数据' # 发送的信息
    # 1. 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 绑定本地信息
    udp_socket.bind(("", 8888))

    # 循环用来接收信息
    while True:
        # 3. 接收数据
        #  1024表示本次接收的最大字节数, 必须大于发送的数据大小，不然报错
        recv_msg = udp_socket.recvfrom(1024)
        # 4. 解码
        recv_ip = recv_msg[1] # 获取客户端的ip和端口号
        recv_msg = recv_msg[0].decode("utf-8") # 获取客户端发送的信息
        # 5. 显示接收到的数据
        print(">>>%s:%s" % (str(recv_ip), recv_msg))
        # 6. 发送数据
        udp_socket.sendto(msg.encode("utf-8"), recv_ip)

if __name__ == "__main__":
    main()