import json
import matplotlib.pyplot as plt
import skimage.io as io
import cv2
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

import cv2 # C:\\Program Files (x86)\\BMDownload\\Rectangle_btiff_卫图\\Rectangle_btiff_卫图_Level_18zhuancgcs2.tif
gdal.AllRegister()

# from labelme import utils
print('json to geojson')
# def main():
json_path = 'D:/111/Rectangle_taishun_train/Rectangle_vaild_Level_18.json'
data = json.load(open(json_path,encoding='utf-8'))
# print(data)
# img = cv2.imread('D:/111/Rectangle_ceshi/Rectangle_ceshi_Level_18.tif', 0)
# lab, lab_names = utils.labelme_shapes_to_label(img.shape, data['shapes']) 
# captions = ['%d: %s' % (l, name) for l, name in enumerate(lab_names)]
# lab_ok = utils.draw_label(lab, img, captions)
a = data['shapes']
print(len(a), len(a[0]), a[1], len(a[1]), a[0]['points'], len(a[0]['points']))
# a[0]['points'].append(a[0]['points'][0])
# print(a[0]['points'])

loadData = gp.read_file("cla/00.geojson")

ab, b = [], []
for i in range(len(a)):
    # if i > 3:
    #     break
    coords = []
    transformedList = []
    a[i]['points'].append(a[i]['points'][0])
    coords.append(a[i]['points'])
    currentPolygon = np.array(coords)
    print('coords :: i', i, np.array(coords), currentPolygon.shape)
    for j in range(currentPolygon.shape[1]):
        print('currentPolygon.shape: i, j',i,j, currentPolygon.shape[1], currentPolygon[0][j][0], currentPolygon[0][j][1])
        transformedList.append(Point(currentPolygon[0][j][1], currentPolygon[0][j][0]))
        ab.append(currentPolygon[0][j][0])
        b.append(currentPolygon[0][j][1])
        print(Point(currentPolygon[0][j][0], currentPolygon[0][j][1]))
    # currentGeometry = loadData.loc[i, 'geometry']
    transformedPoint = Polygon(transformedList)
    
    # 用转换后的坐标替换原来的坐标
    loadData.loc[i, 'geometry'] = transformedPoint
# plt.subplot(121)
# plt.imshow(img)
# plt.subplot(122)
# plt.imshow(lab_ok)
# plt.show()
print(max(ab), max(b))
loadData.to_file("cla/0vaild.geojson", driver='GeoJSON', encoding="GB2312")

# if __name__ == '__main__':
#     main()