from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
while 1:
    # print("please input a:")
    a = input('> ')
    # print("please input b:")
    # b = input('> ')
    # if not b:
    #     break
    if not a:
        break
    tcpCliSock.send(bytes(a.encode()))
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))
tcpCliSock.close()
