from skimage.metrics import structural_similarity
import argparse
import imutils
import cv2

# 找两张图的相似
# 加载两张图片：
# 注意，从文件路径复制来的斜杠是反的，记得更改，且用英文路径，图片格式为jpg,否则会报错

imageA = cv2.imread("D:/32b8c2133a3c76fa156bf2bf96414ba.jpg")
imageB = cv2.imread("D:/c56e43c95e0b92031ac7b9a9bd2ea85.jpg")

# 将他们转换为灰度：

grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# 计算两个灰度图像之间的结构相似度指数：
# 不过ssim多用于压缩图片后的失真度比较。。

(score, diff) = structural_similarity(grayA, grayB, full=True)
# cv2.imshow("diff1", diff)

# diff是一张图，score是指数，score越低说明两张图差异越大

diff = (diff * 255).astype("uint8")  # 小数转int
# cv2.imshow("diff2", diff)

# 找到不同点的轮廓以致于我们可以在被标识为“不同”的区域周围放置矩形：

thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# cv2.imshow("thresh", thresh)
# 阈值的作用是根据设定的值处理图像的灰度值，比如灰度大于某个数值像素点保留。通过阈值以及有关算法可以实现从图像中抓取特定的图形，比如去除背景等。
# threshold会返回两个值，下标为1的是二值化图片
# 所以现在这个thresh图，是个非黑即白的图

# cv2.findContours()函数返回两个值，一个是轮廓本身，还有一个是每条轮廓对应的属性。
# 其首先返回一个list，list中每个元素都是图像中的一个轮廓(也就是一个图)
# 第一个参数是原图经过灰度化和二值化处理后的图


cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# cv2.RETR_EXTERNAL 只检测外轮廓
# cv2.RETR_LIST 提取所有轮廓，并放置在list中，检测的轮廓不建立等级关系
# cv2.RETR_CCOMP 建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
# cv2.RETR_TREE 检测所有轮廓，建立完整的层次结构，建立网状轮廓结构


"""注意cv版本，下面这一行会出现下列问题：
OpenCV 3 改为cv2.findContours(...)返回值为image, contours, hierarchy，

OpenCV 2 cv2.findContours(...)和OpenCV 4 的cv2.findContours(...)返回值为contours, hierarchy。"""

# 把contour轮廓储存在cnts这个list列表里

cnts = cnts[1] if imutils.is_cv2() else cnts[0]

# 找到一系列区域，在区域周围放置矩形：
"""

cv2.rectangle(imageA,(x,y),(x+w,y+h),(0,0,255),2)  参数解释

第一个参数：img是原图

第二个参数：（x，y）是矩阵的左上点坐标

第三个参数：（x+w，y+h）是矩阵的右下点坐标

第四个参数：（0,0,255）是画线对应的rgb颜色

第五个参数：2是所画的线的宽度
"""

for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

# 用cv2.imshow 展现最终对比之后的图片， cv2.imwrite 保存最终的结果图片

cv2.imshow("differ", imageB)
cv2.imwrite("differ.png", imageB)
cv2.waitKey(0)
