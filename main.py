import socket
from socket import *
from time import ctime
import re
import select

# tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
CONFORM_MSG = re.compile(r'^<RID:(\d+)>([\s\S]*?)</RID:\1>')

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(10)

_current_in_list = [tcpSerSock]
_room = dict()


def broadcast_message(room_id, sock, message):
    for member in _room[room_id]:
        if member is not sock:
            try:
                member.send(message)
            except socket.error:
                member.close()
                _current_in_list.remove(member)
                _room[room_id].remove(member)


while 1:
    print("waiting for connection...")
    tcpCliSock, addr = tcpSerSock.accept()
    print("...connected from:", addr)
    while 1:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        print(ctime() + "\n" + data.decode())
        s = input('> ')
        if not s:
            break

        # data = int(s[0]) + int(s[1])
        tcpCliSock.send(bytes(ctime() + "\n" + s, 'utf-8'))
        # cpCliSock.send(bytes(, 'utf-8'))
    tcpCliSock.close()
tcpSerSock.close()









