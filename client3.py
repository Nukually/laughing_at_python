from threading import Thread
from socket import *
import time

tcpClientSocket = None


# 接收服务器数据
def recvData():
    global tcpClientSocket
    while True:
        recvData = tcpClientSocket.recv(1024)
        if len(recvData) == 0:
            print('服务器已关闭！')
            tcpClientSocket.close()
            break
        print(recvData.decode())
        time.sleep(1)


# 发送数据
def sendData():
    global tcpClientSocket
    while True:
        sendData = input("")
        tcpClientSocket.send(sendData.encode())


def main():
    global tcpClientSocket
    tcpClientSocket = socket(AF_INET, SOCK_STREAM)
    serverIP = input("请输入服务器ip: ")
    serverPort = input("请输入服务器端口号: ")
    serverAdd = (serverIP, int(serverPort))
    tcpClientSocket.connect(serverAdd)

    tr = Thread(target=recvData)
    ts = Thread(target=sendData)

    tr.start()
    ts.start()

    tr.join()
    ts.join()

    tcpClientSocket.close()


if __name__ == "__main__":
    main()
