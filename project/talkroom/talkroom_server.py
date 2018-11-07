# coding = utf-8
'''
Talkroom
env:python 3.5
socket and fork
'''

from socket import *
import os, sys

def do_login(s, user, name, addr):
    if (name in user) or name == '管理员':
        s.sendto('该用户已存在!!!'.encode(), addr)
        return
    s.sendto(b'ok',addr)
    # 通知其他人
    msg = '\n欢迎%s进入聊天室'%name
    for i in user:
        s.sendto(msg.encode(), user[i])
    # 将用户加入user
    user[name] = addr

def do_chat(s, user, name, msg):
    msg = '\n%s说:%s'%(name, msg)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])

def do_quit(s, user, name):
    msg = '\n%s退出了聊天室'%name
    for i in user:
        if i == name:
            s.sendto(b'EXIT', user[i])
        else:
            s.sendto(msg.encode(), user[i])
    del user[name]

def do_request(s):
    user = {}
    while True:
        msg, addr = s.recvfrom(1024)
        msgList = msg.decode().split(' ')
        if msgList[0] == 'L':
            do_login(s, user, msgList[1], addr)
        elif msgList[0] == 'C':
            # 重新组织消息
            msg = ' '.join(msgList[2:])
            do_chat(s, user, msgList[1], msg)
        elif msgList[0] == 'Q':
            do_quit(s, user, msgList[1])


# 创建网络连接
def main():
    ADDR = ('0.0.0.0',6969)
    # 创建套接字
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)

    # 用于接收各种客户端请求,调用相应的函数处理

    pid = os.fork()
    if pid < 0:
        print('创建进程失败')
        return
    elif pid == 0:
        while True:
            msg = input('输入管理员消息:')
            msg = 'C 管理员 ' + msg
            s.sendto(msg.encode(), ADDR)
    else:
        do_request(s)



if __name__ == '__main__':
    main()