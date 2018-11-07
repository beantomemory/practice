#coding=utf-8
'''
电子词典 客户端
'''

from socket import *
import sys


class Dictlient():
    def __init__(self, address):
        self.s = socket()
        self.s.connect(address)

def main():
    if len(sys.argv) < 3:
        print('argv is Error!')
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    clientd = Dictlient(ADDR)