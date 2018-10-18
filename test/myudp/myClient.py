#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket

def main():
    print('zou')
    msg = 'herehereherehereherehere' # 发送的信息
    server_ip = '127.0.0.1' # 服务端的ip
    server_port = 8888 # 服务端的端口号
    # 1. 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 发送数据
    udp_socket.sendto(msg.encode("utf-8"), (server_ip, server_port))
    # 循环用来接收信息
    while True:
        # 从服务器段接收数据可以直接用 recv() 只接收内容，而不用管IP，因为已经知道服务端的ip了
        # 3. 接收数据
        recv_msg = udp_socket.recvfrom(102400)
        # 4. 解码
        recv_ip = recv_msg[1] # 获取服务器的ip和端口号
        recv_msg = recv_msg[0].decode("utf-8") # 获取服务器发送的信息
        # 5. 显示接收到的数据
        print(">>>%s:%s" % (str(recv_ip), recv_msg))

if __name__ == "__main__":
    main()