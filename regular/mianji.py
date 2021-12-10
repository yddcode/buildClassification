import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimage
from skimage import io 
import numpy as np
img = io.imread('labels5reg.jpg', as_gray=True)
img = cv2.medianBlur(img, 5)
# img = io.imread('labels3.tif')
# img = mpimage.imread('label3.png')
# mpimage.imsave()
# img = cv2.imread('lable3.png', 0)
# plt.imshow(img)
# plt.show()
print(img.shape)

fill_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

contours,hierarchv = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
# img = cv2.drawContours(img,contours,-1,255,3)
hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in contours] # 绘制文本区域
# cv2.polylines(img, hulls, 1, 255, 3)
# plt.imshow(img)
# plt.show()
# img = img[:2000,:2000]
# cv2.namedWindow("vis",0)
# cv2.resizeWindow("vis", 1000, 900)
# cv2.imshow('vis', img)
# cv2.waitKey()


areas = []
a, b, c, d = [], [], [], []
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    areas.append(area)
    if area*0.53*0.53<3:
      cv2.drawContours(fill_img,contours,i,(255,255,0),-1)
      a.append(area*0.53*0.53)
    if area*0.53*0.53>3 and area*0.53*0.53<100:
      cv2.drawContours(fill_img,contours,i,(0,0,255),-1)
      b.append(area*0.53*0.53)
    if area*0.53*0.53<200 and area*0.53*0.53>100:
      cv2.drawContours(fill_img,contours,i,(0,255,0),-1)
      c.append(area*0.53*0.53)
    if area*0.53*0.53>200:
      cv2.drawContours(fill_img,contours,i,(255,0,0),-1)
      d.append(area*0.53*0.53)

cv2.imwrite('labels5cont.png', fill_img)

print(len(contours), len(areas), areas,'\n',a, b, c, d,'\n',len(a),len(b),len(c),len(d))
