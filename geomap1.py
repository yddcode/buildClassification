# 导入Geopandas
import gdal # 依赖包
import fiona
import shapely
import pyproj
import geopandas as gp
from osgeo import gdal
from osgeo import osr
import numpy as np
from transform import geo2imagexy, lonlat2geo, imagexy2geo, geo2lonlat

# 引入地理坐标系转换功能包
# from gc_method import CoorChange as cc
from coord_convert.transform import wgs2gcj, wgs2bd, gcj2wgs, gcj2bd, bd2wgs, bd2gcj 
# 引入Point类型
from shapely.geometry import Point, Polygon#, geometry

import cv2 # C:\\Program Files (x86)\\BMDownload\\Rectangle_btiff_卫图\\Rectangle_btiff_卫图_Level_18zhuancgcs2.tif
gdal.AllRegister() # C:\Program Files (x86)\BMDownload\Rectangle_btiff_卫图
file_path = 'D:/111/Rectangle_taishun_train/Rectangle_vaild_Level_18.tif'#"C:\\Program Files (x86)\\BMDownload\\Rectangle_c3_卫图\\Rectangle_c3_卫图_Level_18.tif"./cla/sum/c3.tif
dataset = gdal.Open(file_path)

# 读取Shapefile文件./cla/Rectangle_1.shp   ./cla/sum/cuiyuan_xy_after0test.geojson D:/111/Rectangle_xihuLK/Rectangle_xihuLK.shp
loadData = gp.read_file("cla/0vaild.geojson") # .dbf prj shap shx tdb D:/work/Rectangle_c3shapewgs84_建筑轮廓/Rectangle_c3shapewgs84_建筑轮廓.shp
print("读取的数据：")
print(loadData)

# 判断Shapefile文件的格式，有点、线、面三种
loadType = loadData['geometry'][0].geom_type
print("空间数据类型：")
print(loadType)

def check(currentPolygon):
    ch = 0
    zong = []
    for j in range(0, len(currentPolygon)):
      zong.append(int(currentPolygon[j][0]))

    print(currentPolygon[0],currentPolygon[0][0],currentPolygon[0][1],zong,ch)
    if ch not in zong:
      print('不在', zong,ch)
      return True
    else:
      print('zai', zong,ch,zong[0]==0)
      return False

for i in range(0, len(loadData)):
    # if i > 15:
    #     break
    # 读取当前点数据
    print(i)
    
    currentGeometry = loadData.loc[i, 'geometry']
    # 读取当前点的经度和纬度
    # currentLon = currentGeometry.x
    # currentLat = currentGeometry.y
     # 读取当前面的每个坐标点
    currentPolygon = currentGeometry.exterior.coords
    # print(currentPolygon, len(currentPolygon))
    transformedList = []
    # for jc in range(0, len(currentPolygon)):
    # if check(currentPolygon):
    #     for j in range(0, len(currentPolygon)):
    #         # transformedResult = geo2imagexy(dataset, currentPolygon[j][0], currentPolygon[j][1])
    #         transformedResult = imagexy2geo(dataset, currentPolygon[j][0], currentPolygon[j][1])
    #         transformedList.append(Point(transformedResult[0], transformedResult[1]))
    # else:
    #     break
        # print(transformedResult[0], transformedResult[1], currentPolygon[j][0], currentPolygon[j][1])

    # 进行地理坐标系转换
    # transformedResult = cc.main(currentLon, currentLat, originCoordSystem, afterCoordSystem)
    # print(transformedList)
    for j in range(len(currentPolygon)):
        transformedResult = imagexy2geo(dataset, currentPolygon[j][0], currentPolygon[j][1])
        transformedResult = geo2lonlat(dataset, transformedResult[0], transformedResult[1])
        # transformedResult = lonlat2geo(dataset, currentPolygon[j][1], currentPolygon[j][0])
        # transformedResult = geo2imagexy(dataset, transformedResult[0], transformedResult[1])
        transformedList.append(Point(transformedResult[1], transformedResult[0]))

        print(currentPolygon[j][1], Point(transformedResult[0], transformedResult[1]))
    # 生成转换之后的点数据
    transformedPoint = Polygon(transformedList)
    # 用转换后的坐标替换原来的坐标
    loadData.loc[i, 'geometry'] = transformedPoint
    
loadData.to_file("cla/0vaildjwzb.geojson", driver='GeoJSON', encoding="GB2312")


