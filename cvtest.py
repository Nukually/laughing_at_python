import cv2
import numpy as np
import threading
from skimage.metrics import structural_similarity
import time
from multiprocessing import Process, Queue
import os, time, random
import imutils


class Camera(threading.Thread):
    __slots__ = ['camera', 'Flag', 'count', 'width', 'heigth', 'frame']

    def __init__(self):
        threading.Thread.__init__(self)
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.Flag = 0
        self.count = 1
        self.width = 1920
        self.heigth = 1080
        self.name = ''
        self.path = ''
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.heigth)
        # for i in range(46):
        # print("No.={} parameter={}".format(i,self.camera.get(i)))

    def run(self):
        while True:
            ret, self.frame = self.camera.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。 frame为视频的每一帧图像
            self.frame = cv2.flip(self.frame, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示。
            if self.Flag == 1:
                print("拍照")
                if self.name == '' and self.path == '':
                    cv2.imwrite(str(self.count) + '.jpg', self.frame)  # 将画面写入到文件中生成一张图片
                elif self.name != '':
                    cv2.imwrite(self.name + '.jpg', self.frame)
                self.count += 1
                self.Flag = 0
            if self.Flag == 2:
                print("退出")
                self.camera.release()  # 释放内存空间
                cv2.destroyAllWindows()  # 删除窗口
                break

    def take_photo(self):
        self.Flag = 1

    def exit_program(self):
        self.Flag = 2

    def set_name(self, str):
        self.name = str

    def set_path(self, str):
        self.path = str


def comparation(imageA, imageB):
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1] if imutils.is_cv2() else cnts[0]
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return imageB


def show_window(cap):
    while True:
        cv2.namedWindow("window", 1)  # 1代表外置摄像头
        cv2.resizeWindow("window", cap.width, cap.heigth)  # 指定显示窗口大小
        imageB = cap.frame
        imageA = cv2.imread("1.jpg")
        imageC = comparation(imageA, imageB)
        cv2.imshow('window', imageC)
        c = cv2.waitKey(50)  # 按ESC退出画面
        if c == 27:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    cap = Camera()
    cap.start()
    while True:
        i = int(input("input:"))
        if i == 1:
            cap.take_photo()
        if i == 2:
            cap.exit_program()
        if i == 3:
            recv_data_thread = threading.Thread(target=show_window, args=(cap,))
            recv_data_thread.start()
        time.sleep(1)
