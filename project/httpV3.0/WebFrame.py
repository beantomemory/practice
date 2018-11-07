#coding=utf-8
'''
This is WebFrame
'''
from socket import *
from settings import *
import sys
from threading import Thread

# 应用类, 将功能封装在类中
class WebServer(object):
    def __init__(self, frame_address, static_dir):
        self.frame_address = frame_address
        self.static_dir = static_dir
        self.create_socket()
        self.bind(frame_address)

    def create_socket(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self, frame_address):
        self.ip = frame_address[0]
        self.port = frame_address[1]
        self.s.bind(frame_address)

    def serve_forever(self):
        self.s.listen(10)
        print('WebFrame listen the port: %d'%self.port)
        while True:
            try:
                c, addr = self.s.accept()
                print('WebFrame connect from:', addr)
            except KeyboardInterrupt:
                self.s.close()
                sys.exit('WebFrame服务端退场~~')
            except Exception as e:
                print('Error:', e)
                continue
        
            clientThread = Thread(target = self.handle, args = (c,))
            clientThread.setDaemon(True)
            clientThread.start()

    def handle(self, c):
        request = c.recv(4096).decode()
        if not request:
            c.close()
            return
        dic = eval(request)
        print('server request:', dic)
        if dic['PATH_INFO'] == '/':
            filename = self.static_dir + '/index.html'
        else:
            filename = self.static_dir + dic['PATH_INFO']

        print(filename)

        try:
            f = open(filename)
        except Exception:
            responseHeaders = 'HTTP/1.1 404 Not found\r\n'
            responseHeaders += '\r\n'
            responseBody = 'Sorry, not found the page'
        else:
            # 如果找到网页则返回网页
            responseHeaders = 'HTTP/1.1 200 OK\r\n'
            responseHeaders += '\r\n'
            responseBody = f.read()
        finally:
            response = responseHeaders + responseBody
            c.send(response.encode())


if __name__ == '__main__':
    static_dir = './static'
    webd = WebServer(frame_address, static_dir)
    webd.serve_forever()