#coding=utf-8
'''
aid httpserver v3.0
'''

from socket import *
import sys
from threading import Thread
from settings import *
import re
import time

# # 和 WebFrame 通信
# def connect_frame(connfd, env):
#     s = socket()
#     s.connect(frame_address) # 连接框架服务器地址
#     s.send(str(env).encode()) # 向webframe发送请求
#     Web_data = s.recv(4096) # 接受web返回数据
#     connfd.send(Web_data) # 向浏览器发送响应
#     connfd.close()
    
# 和 WebFrame 通信
def connect_frame(METHOD, PATH_INFO):
    s = socket()
    try:
        s.connect(frame_address) # 连接框架服务器地址
    except Exception as e:
        print('Connect error:', e)
        return
    s.send(METHOD.encode()) # 向webframe发送请求
    time.sleep(0.1)
    s.send(PATH_INFO.encode()) # 向webframe发送请求
    response = s.recv(4096).decode()
    if not response:
        response ='404'
    s.close()
    return response

# 封装httpserver类
class HTTPServer(object):
    def __init__(self, address):
        self.address = address
        self.create_socket()
        self.bind(address)

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 绑定地址
    def bind(self, address):
        self.ip = address[0]
        self.port = address[1]
        self.sockfd.bind(address)

    def serve_forever(self):
        self.sockfd.listen(10)
        print('Listen the port %d'%self.port)
        while True:
            try:
                connfd, addr = self.sockfd.accept()
                print('Connect from:', addr)
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('服务器退场哒')
            except Exception as e:
                print('Error:', e)
                continue
        
            clientThread = Thread(target = self.handle, args = (connfd,))
            clientThread.setDaemon(True)
            clientThread.start()

    def handle(self, connfd):
        # 接受浏览器发来的http请求
        request = connfd.recv(4096)
        if not request:
            connfd.close()
            return
        request_lines = request.splitlines()

        request_line = request_lines[0].decode('utf-8')
        print(request_line)

        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'
        try:
            env = re.match(pattern, request_line).groupdict()
            print(env)
        except:
            response_headlers = 'HTTP/1.1 500 SERVER ERROR\r\n'
            response_headlers += '\r\n'
            response_body = 'Server Error'
            response = response_headlers + response_body
            connfd.send(response.encode())
            connfd.close()
            return
        
        response = connect_frame(**env)
        if response == '404':
            response_headlers = 'HTTP/1.1 404 Not Found\r\n'
            response_headlers += '\r\n'
            response_body = '===Sorry, not found the page==='
        else:
            response_headlers = 'HTTP/1.1 200 OK\r\n'
            response_headlers += '\r\n'
            response_body = response
        response = response_headlers + response_body
        connfd.send(response.encode())
        connfd.close()
        


if __name__ == '__main__':
    httpd = HTTPServer(ADDR)
    httpd.serve_forever() # 启动http服务