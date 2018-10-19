from socket import *

# 创建socket
tcp_client_socket = socket(AF_INET, SOCK_STREAM)

# 目的信息
# ip 或 域名
server_ip = '127.0.0.1'
# 端口号
server_port = 8808

# 连接服务器
tcp_client_socket.connect((server_ip, server_port))

# 提示用户输入数据
send_data = 'here'

tcp_client_socket.send(send_data.encode("utf-8"))


# 接收对方发送过来的数据，最大接收1024个字节
recvData = tcp_client_socket.recv(1024)
print('接收到的数据为:', recvData.decode('utf-8'))
send_data = 'i here'
tcp_client_socket.send(send_data.encode("utf-8"))
# 关闭套接字
tcp_client_socket.close()