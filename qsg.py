from threading import Thread
from socket import *
import time

tcpSocket = None
aliveConnList = []


# 接受新连接线程
def acceptConn():
    global aliveConnList
    global tcpSocket
    while True:
        newSocket, clientAddr = tcpSocket.accept()
        print('%s已连接' % (str(clientAddr)))
        newSocket.settimeout(1)
        aliveConnList.append((newSocket, clientAddr))


# 接收新消息线程
def recvData():
    global aliveConnList
    while True:
        # 遍历缓冲区，有数据输出并转发，没数据超时过
        for s in aliveConnList:
            try:
                # print("receiving")
                recvData = s[0].recv(1024)
                # print("received")
                if len(recvData) > 0:
                    # 有数据，向其他tcp发送该数据
                    for other in aliveConnList:
                        if other != s:
                            other[0].send(('recv from %s:%s' % (s[1], recvData.decode())).encode())
                    print('recv from %s:%s' % (s[1], recvData.decode()))
                else:
                    # 客户端断开
                    print('%s已断开连接' % (str(s[1])))
                    s[0].close()
                    aliveConnList.remove(s)
            except timeout:
                # 该连接无数据
                pass
        # 可怜的cpu
        time.sleep(1)


# def sendData():
#     global tcpSocket
#     while True:
#         sData = input("")
#         tcpSocket.send(sData.encode())


def main():
    global tcpSocket
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    address = ('', 1234)
    tcpSocket.bind(address)
    tcpSocket.listen(5)

    print("欢迎使用")

    ta = Thread(target=acceptConn)
    tr = Thread(target=recvData)
    # ts = Thread(target=sendData)

    ta.start()
    tr.start()
    # ts.start()

    ta.join()
    tr.join()
    # ts.join()

    tcpSocket.close()


if __name__ == "__main__":
    main()
