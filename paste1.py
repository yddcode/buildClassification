# coding=utf-8
import cv2
import numpy as np
import os
import math
# ./cla/Rectangle_bbulid_/_ArcGis/_alllayers/L18/ Rectangle_c3wapian18fentuceng_
rootdir = './cla/wenxin/_ArcGis/_alllayers/L18/'
imgs, path = [], []
i = 0
# 120.14639854431152,30.18467903137207 120.19781112670898,30.18467903137207 120.19781112670898,30.142621994018555 120.14639854431152,30.142621994018555 120.14639854431152,30.18467903137207
rows, cols = [], []
for parent, dirname, filenames in os.walk(rootdir):
    print(parent, dirname, filenames)
    if i == 0:
        row = len(dirname)
        rows.append(row)
        print('row:', row)
    if i > 0:
        col = len(filenames)
        cols.append(col)
        print('col', len(filenames))
    
    for filename in filenames:
        if filename.endswith('jpg'):

            # name = os.path.join(parent, filename)
            name = parent + '/'+filename
            print(name)
            # 读取瓦片
            img = cv2.imread(name)
            # 附加到list
            imgs.append(img)
            path.append(name)
            # cv2.imshow('img1', img)
            # cv2.waitKey(0)
    i = i + 1
row, col = np.max(rows), np.max(cols)
cols_sum = np.sum(cols)
num = row*cols_sum
temp = np.zeros((row*256, col*256, 3), dtype=np.uint8)
h, w, _ = temp.shape
# for i in range(h):
#     for j in range(w):
#         temp[i,j,:] = 255    
print('Images are loaded.', temp.shape, row,col,rows,cols, cols_sum,num, len(imgs))
sum = 0
for i in range(row):
    
    for j in range(cols[i]):#col
        
        # print(imgs[i*col+j], i*col+j, i,(i+1)*256, j,(j+1)*256)
        # temp[i*256:(i+1)*256, j*256:(j+1)*256, :] = imgs[i*col+j]
        temp[i*256:(i+1)*256, j*256:(j+1)*256, :] = imgs[sum+j]
    sum = sum + cols[i]
    print(sum)

cv2.imshow('img', temp)
cv2.waitKey(0)
cv2.imwrite('./cla/sum/wenxin.tif', temp)