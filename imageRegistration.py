# 导入Geopandas
import gdal # 依赖包
import fiona
import shapely
import pyproj
import geopandas as gp
from osgeo import gdal
from osgeo import osr
import numpy as np
from transform import geo2imagexy, lonlat2geo, imagexy2geo

# 引入地理坐标系转换功能包
# from gc_method import CoorChange as cc
from coord_convert.transform import wgs2gcj, wgs2bd, gcj2wgs, gcj2bd, bd2wgs, bd2gcj 
# 引入Point类型
from shapely.geometry import Point, Polygon#, geometry
# 傣族古籍文字切分作为OCR识别系统的前期工作
import cv2 # C:\\Program Files (x86)\\BMDownload\\Rectangle_btiff_卫图\\Rectangle_btiff_卫图_Level_18zhuancgcs2.tif
gdal.AllRegister() # C:\Program Files (x86)\BMDownload\Rectangle_btiff_卫图
file_path = 'D:/111/翠苑街道_卫图/翠苑街道_卫图_Level_18.tif'#"C:\\Program Files (x86)\\BMDownload\\Rectangle_c3_卫图\\Rectangle_c3_卫图_Level_18.tif"./cla/sum/c3.tif
dataset = gdal.Open(file_path)
print(dataset)
# 读取Shapefile文件./cla/Rectangle_1.shp  D:/111/翠苑街道_建筑轮廓/翠苑街道_建筑轮廓.shp
loadData = gp.read_file("./cla/sum/cuiyuan_xy_after.geojson") # .dbf prj shap shx tdb D:/work/Rectangle_c3shapewgs84_建筑轮廓/Rectangle_c3shapewgs84_建筑轮廓.shp
print("读取的数据：")
print(loadData)

# 判断Shapefile文件的格式，有点、线、面三种
loadType = loadData['geometry'][0].geom_type
print("空间数据类型：")
print(loadType)

img = cv2.imread('D:/111/Level_18.tif', 1)
mask = cv2.imread('./cla/sum/cuiyuan_mask1.jpg', 1)
h, w, c = mask.shape
# cv2.imshow('img', img)
# cv2.imshow('mask', mask)
# cv2.waitKey(0)

print(mask.shape)
# querySer = loadData.loc[:, 'geometry'] > 0
# #应用查询条件
# print('删除异常值前：',loadData.shape)
# DataDF = loadData.loc[querySer,:]
# print('删除异常值后：',DataDF.shape)
loadData0 = gp.read_file("./cla/00.geojson")
# for i in range(0, len(loadData0)):
#     # if i == 1:
#     #     break
#     # 读取当前点数据
#     # print(i)
#     currentGeometry = loadData.loc[i, 'geometry']
#     # 读取当前点的经度和纬度
#     # currentLon = currentGeometry.x
#     # currentLat = currentGeometry.y
#      # 读取当前面的每个坐标点
#     currentPolygon = currentGeometry.exterior.coords
#     # print(currentPolygon, len(currentPolygon))
#     transformedList = []
#     for j in range(0, len(currentPolygon)):
#       transformedList.append(Point(0, 0))
#         # print(transformedResult[0], transformedResult[1], currentPolygon[j][0], currentPolygon[j][1])

#     # 进行地理坐标系转换
#     # transformedResult = cc.main(currentLon, currentLat, originCoordSystem, afterCoordSystem)
#     # print(transformedList)
    
#     # 生成转换之后的点数据
#     transformedPoint = Polygon(transformedList)
#     # 用转换后的坐标替换原来的坐标
#     loadData0.loc[i, 'geometry'] = transformedPoint
#     # print(transformedList)

# loadData0.to_file("./cla/00.geojson", driver='GeoJSON', encoding="GB2312")
b = 0
for i in range(1000, len(loadData)-1400):
    # if i > 10:
    #     break
    # 读取当前点数据
    print(i)
    
    print(mask.shape)
    currentGeometry = loadData.loc[i, 'geometry']
    # 读取当前点的经度和纬度
    # currentLon = currentGeometry.x
    # currentLat = currentGeometry.y
     # 读取当前面的每个坐标点
    currentPolygon = currentGeometry.exterior.coords
    # print(currentPolygon, len(currentPolygon))
    transformedList = []
    arr = np.array([255,255,255])
    lenpoly = len(currentPolygon)
    a = 0  
    for j in range(0, len(currentPolygon)):
              
        print(currentPolygon[j][0], currentPolygon[j][1], img[4, 582,:]== [255,255,255], img[10, 10], mask[10, 10], np.bitwise_and(img[4, 582,:], [255,255,255]), lenpoly)
        if currentPolygon[j][0] < 0 or currentPolygon[j][1] < 0:
            print('currentPolygon[j][0] < 0 or currentPolygon[j][1] < 0:', currentPolygon[j][0], currentPolygon[j][1], lenpoly)
            lenpoly = lenpoly - 1
            if lenpoly < 3:
                b = b + 1
                break
            # break
            # currentPolygon[j][0], currentPolygon[j][1] = 0, 0
            # transformedList.append(Point(0, 0))
        elif currentPolygon[j][0] > w or currentPolygon[j][1] > h:
            print('currentPolygon[j][0] > h or currentPolygon[j][1] > w:', currentPolygon[j][0], currentPolygon[j][1], lenpoly, h,w)
            lenpoly = lenpoly - 1
            if lenpoly < 3:
                b = b + 1
                break
            # break
            # currentPolygon[j][0], currentPolygon[j][1] = 0, 0
            # transformedList.append(Point(0, 0))
        elif (img[int(currentPolygon[j][1]),int(currentPolygon[j][0]),:] == arr).any()==True and (mask[int(currentPolygon[j][1]),int(currentPolygon[j][0])] == arr).any()==True:
            print('img mask :', img[int(currentPolygon[j][1]),int(currentPolygon[j][0]),:], mask[int(currentPolygon[j][1]),int(currentPolygon[j][0])], lenpoly)
            lenpoly = lenpoly - 1
            if lenpoly < 3:
                b = b + 1
                break
            # currentPolygon[j][0], currentPolygon[j][1] = 0, 0
            # transformedList.append(Point(0, 0))
            # break
        # elif lenpoly < 3:
        #     break
        # else:
        #     print('calu::', lenpoly)
        #     a = a + 1
        #     if a < 3:
        #       break
            # transformedResult = imagexy2geo(dataset, currentPolygon[j][0], currentPolygon[j][1])
            # transformedList.append(Point(transformedResult[0], transformedResult[1]))
        else:
            a = a + 1
            print('a', a)
            transformedList.append(Point(currentPolygon[j][0], currentPolygon[j][1]))
        
        # print(transformedResult[0], transformedResult[1], currentPolygon[j][0], currentPolygon[j][1])

    # 进行地理坐标系转换
    # transformedResult = cc.main(currentLon, currentLat, originCoordSystem, afterCoordSystem)
    # print(transformedList)
        
        if a > 2:
            print('a>2 ',a)
            
            # 生成转换之后的点数据
            transformedPoint = Polygon(transformedList)
            # 用转换后的坐标替换原来的坐标
            loadData0.loc[i, 'geometry'] = transformedPoint
        else:
          print('b', b)
          b = b + 1
          break
    print(i-b)
    
    # print(transformedList)
    

loadData0.to_file("./cla/sum/cuiyuan_xy_after0test.geojson", driver='GeoJSON', encoding="GB2312")