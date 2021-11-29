# from shapely.geometry import Point, Polygon#, geometry
# 导入Geopandas 4385 5355 3348 4255 960 5180+175 855 4170+215
import gdal # 依赖包
import fiona
import shapely
import pyproj
import geopandas as gp
from osgeo import gdal
from osgeo import osr
import numpy as np
from transform import geo2imagexy, lonlat2geo
import cv2

import numpy as np
import matplotlib.pyplot as plt
# data = [(596,221),(597,233),(591,245),(589,256),(584,255),(580,249),(590,233),(593,225)]
# 读取Shapefile文件./cla/Rectangle_1.shp
loadData = gp.read_file("./cla/sum/cuiyuan_xy_after.geojson") # .dbf prj shap shx tdb
print("读取的数据：")
print(loadData)

# 判断Shapefile文件的格式，有点、线、面三种
loadType = loadData['geometry'][0].geom_type
print("空间数据类型：")
print(loadType)

xs, ys, xy = [], [], []
minX, minY, maxX, maxY = [], [], [], []

for i in range(0, len(loadData)):
    # if i == 1:
    #     break
    # 读取当前点数据
    currentGeometry = loadData.loc[i, 'geometry']
    # 读取当前点的经度和纬度
    # currentLon = currentGeometry.x
    # currentLat = currentGeometry.y
     # 读取当前面的每个坐标点
    currentPolygon = currentGeometry.exterior.coords
    # print(currentPolygon, len(currentPolygon))
    transformedList = []
    for j in range(0, len(currentPolygon)):
        x = int(currentPolygon[j][0])
        y = int(currentPolygon[j][1])
        xs.append(x)
        ys.append(y)
    xs = np.vstack((xs))
    ys = np.vstack((ys))
    cor_xy = np.hstack((xs, ys))
    minx = np.min(xs)
    miny = np.min(ys)
    maxx = np.max(xs)
    maxy = np.max(ys)
    minX.append(minx)
    minY.append(miny)
    maxX.append(maxx)
    maxY.append(maxy)
    # print(xs, ys, xy, cor_xy, np.min(minX))
    xs, ys, xy = [], [], []
print(np.min(minX), np.min(minY), np.max(maxX), np.max(maxY))
weight = np.max(maxX) - np.min(minX)
height = np.max(maxY) - np.min(minY)
temp = np.ones((height, weight, 3),np.uint8)*0 #黑色背景
xs, ys, xy = [], [], []
for i in range(0, len(loadData)):
    # if i == 1:
    #     break
    # 读取当前点数据
    currentGeometry = loadData.loc[i, 'geometry']
    # 读取当前点的经度和纬度
    # currentLon = currentGeometry.x
    # currentLat = currentGeometry.y
     # 读取当前面的每个坐标点
    currentPolygon = currentGeometry.exterior.coords
    # print(currentPolygon, len(currentPolygon))
    transformedList = []
    for j in range(0, len(currentPolygon)):
        x = int(currentPolygon[j][0]) - np.min(minX)
        y = int(currentPolygon[j][1]) - np.min(minY)
        xs.append(x)
        ys.append(y)
    xs = np.vstack((xs))
    ys = np.vstack((ys))
    cor_xy = np.hstack((xs, ys))
    # print(xs, ys, xy, cor_xy, np.min(minX))

    cv2.polylines(temp, [cor_xy], True, (255, 255, 255), 3)

    cv2.fillPoly(temp, [cor_xy], (255, 255, 255))
    xs, ys, xy = [], [], []
print(np.min(minX), np.min(minY), np.max(maxX), np.max(maxY))
# for i in range(len(data)):
#     # if i > 2:
#     #     break
#     for j in range(len(data[i])):
#         x = int(data[i][j][0]+100)
#         y = int(data[i][j][1]+100)
#         xs.append(x)
#         ys.append(y)
#         xy.append([x,y])

# plt.scatter(xs,ys,color='r',zorder=2)
# plt.plot(xs,ys,color='b',zorder=1)

# plt.title("Connected Scatterplot points with line")
# plt.xlabel("x")
# plt.ylabel("y")

# x_cor = data['x']
# y_cor = data['y']

# im = np.zeros(图像对应尺寸, dtype="uint8")
    

# temps = cv2.flip(temp, 1)
tempc = cv2.flip(temp, 0)
cv2.imwrite('./cla/sum/cuiyuan_mask.jpg', tempc)
M = cv2.getRotationMatrix2D((height/2, weight/2), -90, 1)
# 参数: 原始图像,旋转参数, 元素图像高度
rotated2 = cv2.warpAffine(tempc, M, (weight, height))
# 显示旋转后的图像
cv2.namedWindow("rotated2", 0)
cv2.resizeWindow("rotated2", 1000,800)
cv2.imshow("rotated2", rotated2)

# tempsc = cv2.flip(temps, 0)

# M = cv2.getRotationMatrix2D((10000/2, 8000/2), 180, 1)
# # 参数: 原始图像,旋转参数, 元素图像高度
# rotated = cv2.warpAffine(temp, M, (10000, 8000))
# # 显示旋转后的图像
# cv2.namedWindow("rotated", 0)
# cv2.resizeWindow("rotated", 1000,800)
# cv2.imshow("rotated", rotated)
# mask_array = temp
# plt.show()
# cv2.drawContours(temp,mask_array,-1,(255,255,255),thickness=-1)
cv2.namedWindow("temp", 0)
cv2.resizeWindow("temp", 1000,800)
cv2.imshow('temp',temp)
cv2.namedWindow("tempc", 0)
cv2.resizeWindow("tempc", 1000,800)
cv2.imshow('tempc',tempc)
# cv2.namedWindow("temps", 0)
# cv2.resizeWindow("temps", 1000,800)
# cv2.imshow('temps',temps)
# cv2.namedWindow("tempsc", 0)
# cv2.resizeWindow("tempsc", 1000,800)
# cv2.imshow('tempsc',tempsc)
cv2.waitKey(0)
# img = cv2.imread('./cla/1.png')
# h,w,_ = img.shape
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# temp = np.ones(gray.shape,np.uint8)*0 #黑色背景
 
# area_1 = Polygon([(596,221),(597,233),(591,245),(589,256),(584,255),(580,249),(590,233),(593,225)])
# bbox = area_1.bounds
# arr_mask = []
# min_x,min_y,max_x,max_y = bbox[0],bbox[1],bbox[2],bbox[3]
# for i in range(int(min_x),int(max_x+1)):
#     for j in range(int(min_y),int(max_y+1)):
#         p_tmp = Point(i,j)
#         if(p_tmp.within(area_1)==True):
#             print(i,j)
#             pos_arr = [[i,j]]
#             arr_mask.append(pos_arr)
            
# mmsk = np.array(arr_mask)
# cv2.drawContours(temp,mmsk,-1,(255,255,255),thickness=-1)
# cv2.imshow('hhh',temp)
# cv2.waitKey(0)