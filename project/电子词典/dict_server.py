#coding=utf-8
'''
电子词典 服务端
'''
from socket import *
from threading import Thread
import sys, os

HOST = '0.0.0.0'
PORT = 6969
ADDR = (HOST, PORT)

class Dictserver():
    def __init__(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind(ADDR)

    def serve_forever(self):
        self.s.listen(5)
        print('Listen the port 6969...')
        while True:
            try:
                c, addr = self.s.accept()
            except KeyboardInterrupt:
                self.s.close()
                sys.exit('servers 退场 洗玛洗哒( ^_^ )/~~')
            except Exception as e:
                print(e)
                continue
            print('Connect from:', addr)

            pid = os.fork()
            if pid == 0:
                p = os.fork()
                if p == 0:
                    s.close()
                    while True:
                        pass
                else:
                    os._exit(0)
            else:
                c.close()
                os.wait()
    
    def handle(self):
        pass
            

if __name__ == '__main__':
    serverd = Dictserver()
    serverd.serve_forever()