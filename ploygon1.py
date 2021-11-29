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

loadData = gp.read_file("cla/00_fanzhuan.geojson") # .dbf prj shap shx tdb
print("读取的数据：")
print(loadData)

# 判断Shapefile文件的格式，有点、线、面三种
loadType = loadData['geometry'][0].geom_type
print("空间数据类型：")
print(loadType)

temp = np.ones((3273, 3613, 3),np.uint8)*0 #黑色背景
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
        x = int(currentPolygon[j][0])# - np.min(minX)
        y = int(currentPolygon[j][1])# - np.min(minY)
        xs.append(x)
        ys.append(y)
    xs = np.vstack((xs))
    ys = np.vstack((ys))
    cor_xy = np.hstack((xs, ys))
    # print(xs, ys, xy, cor_xy, np.min(minX))

    cv2.polylines(temp, [cor_xy], True, (255, 255, 255), 3)

    cv2.fillPoly(temp, [cor_xy], (255, 255, 255))
    xs, ys, xy = [], [], []
# print(np.min(minX), np.min(minY), np.max(maxX), np.max(maxY))
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
# tempc = cv2.flip(temp, 0)
img = cv2.imread('D:/111/Rectangle_ceshi/Rectangle_ceshi_Level_18.tif', 1)
# alpha 为第一张图片的透明度
alpha = 0.5
# beta 为第二张图片的透明度
beta = 0.5
gamma = 0
# cv2.addWeighted 将原始图片与 mask 融合
mask_img = cv2.addWeighted(img, alpha, temp, beta, gamma)

cv2.imwrite('cla/00_mask.png', mask_img)

# cv2.imwrite('cla/00_masktest.jpg', temp)