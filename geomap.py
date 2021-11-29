# 导入Geopandas
import gdal # 依赖包
import fiona
import shapely
import pyproj
import geopandas as gp
from osgeo import gdal
from osgeo import osr
import numpy as np
from transform import geo2imagexy, lonlat2geo

import cv2 # C:\\Program Files (x86)\\BMDownload\\Rectangle_btiff_卫图\\Rectangle_btiff_卫图_Level_18zhuancgcs2.tif
gdal.AllRegister() # C:\Program Files (x86)\BMDownload\Rectangle_btiff_卫图
file_path = "D:\\work\\Rectangle_c3_卫图\\Rectangle_c3_卫图_Level_18.tif"
dataset = gdal.Open(file_path)

# 读取Shapefile文件./cla/Rectangle_1.shp
loadData = gp.read_file("D:/work/Rectangle_c3shapewgs84_建筑轮廓/Rectangle_c3shapewgs84_建筑轮廓.shp") # .dbf prj shap shx tdb
print("读取的数据：")
print(loadData)

# 判断Shapefile文件的格式，有点、线、面三种
loadType = loadData['geometry'][0].geom_type
print("空间数据类型：")
print(loadType)

# 引入地理坐标系转换功能包
# from gc_method import CoorChange as cc
from coord_convert.transform import wgs2gcj, wgs2bd, gcj2wgs, gcj2bd, bd2wgs, bd2gcj 
# 引入Point类型
from shapely.geometry import Point, Polygon#, geometry

originCoordSystem = "GCJ-02"  # 转换前地理坐标系
afterCoordSystem = "WGS-84"  # 转换后地理坐标系

def get_file_info(file_path, dataset):
    pcs, gcs, shape = None, None, None
    '''
    0：图像左上角的X坐标；
    1：图像东西方向分辨率；
    2：旋转角度，如果图像北方朝上，该值为0；
    3：图像左上角的Y坐标；
    4：旋转角度，如果图像北方朝上，该值为0；
    5：图像南北方向分辨率；
    '''
    if file_path.endswith('tif') or file_path.endswith('jpg'):
        # dataset = gdal.Open(file_path)
        dataset = dataset
        pcs = osr.SpatialReference()
        pcs.ImportFromWkt(dataset.GetProjection())
        gcs = pcs.CloneGeogCS()
        extend = dataset.GetGeoTransform()
        shape = (dataset.RasterXSize, dataset.RasterYSize)
    else:
        raise('unsupported file format!')
    return dataset, gcs, pcs, extend, shape

def get_value_by_coordinates(file_path, dataset, coordinates, coordinates_type = 'rowcol'):
    # dataset, gcs, pcs, extend, shape = get_file_info(file_path, dataset)
    pcs, gcs, shape = None, None, None
    if file_path.endswith('tif') or file_path.endswith('jpg'):
        # dataset = gdal.Open(file_path)
        dataset = dataset
        pcs = osr.SpatialReference()
        pcs.ImportFromWkt(dataset.GetProjection())
        gcs = pcs.CloneGeogCS()
        extend = dataset.GetGeoTransform()
        shape = (dataset.RasterXSize, dataset.RasterYSize)
    else:
        raise('unsupported file format!')

    img = dataset.GetRasterBand(1).ReadAsArray()
    value = None
    # print(img, img.shape)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    if coordinates_type == 'rowcol':
        # value = img[int(np.floor(coordinates[1])), int(np.floor(coordinates[0]))], int(np.floor(coordinates[1])), int(np.floor(coordinates[0]))
        value = int(np.floor(coordinates[1])), int(np.floor(coordinates[0]))
    elif coordinates_type == 'lonlat':
        x, y = lonlat2geo(dataset, coordinates[0], coordinates[1])
        row_col = geo2imagexy(dataset, x, y)
        row = int(np.floor(row_col[1]))
        col = int(np.floor(row_col[0]))
        # value = img[row, col], row, col
        value = row, col
    elif coordinates_type == 'xy':
        row_col = geo2imagexy(dataset, coordinates[0], coordinates[1])
        row = int(np.floor(row_col[1]))
        col = int(np.floor(row_col[0]))
        # value = img[row, col], row, col
        value = row, col
    else:
        raise('coordinates_type wrong input!')
    return value

# gdf = gp.GeoDataFrame.from_file(".cla/map.geojson", encoding='gb18030')
# gdf.head()  #输出属性表
# gdf.plot()	#画
# gdf.show()

_, gcs, pcs, extend, _ = get_file_info(file_path, dataset)
# 循环读取每个Geometry
for i in range(0, len(loadData)):
    # if i == 1:
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
    for j in range(0, len(currentPolygon)):
        pixel_value1 = get_value_by_coordinates(file_path,dataset, coordinates=currentPolygon[j], coordinates_type='lonlat')
        xy = lonlat2geo(dataset, currentPolygon[j][0], currentPolygon[j][1])
        pixel_value2 = get_value_by_coordinates(file_path,dataset, coordinates=xy, coordinates_type='xy')
        rowcol = geo2imagexy(dataset, xy[0], xy[1])
        pixel_value3 = get_value_by_coordinates(file_path,dataset, coordinates=rowcol, coordinates_type='rowcol')
        # print('坐标：', currentPolygon[j][0], currentPolygon[j][1], '\n',
        #         '经纬度坐标：', pixel_value1, '\n', 
        #         '投影坐标：', pixel_value2, '\n', 
        #         '图像坐标：', pixel_value3, '\n')
        # 进行坐标系转换
        # transformedResult = cc.main(currentPolygon[j][0], currentPolygon[j][1], originCoordSystem,
        #                       afterCoordSystem)
        # transformedResult = wgs2gcj(currentPolygon[j][0], currentPolygon[j][1])                              
        # transformedResult = geo2imagexy(dataset, currentPolygon[j][0], currentPolygon[j][1])
        transformedList.append(Point(pixel_value3[0], pixel_value3[1]))
        # print(transformedResult[0], transformedResult[1], currentPolygon[j][0], currentPolygon[j][1])

    # 进行地理坐标系转换
    # transformedResult = cc.main(currentLon, currentLat, originCoordSystem, afterCoordSystem)
    # print(transformedList)
    
    # 生成转换之后的点数据
    transformedPoint = Polygon(transformedList)
    # 用转换后的坐标替换原来的坐标
    loadData.loc[i, 'geometry'] = transformedPoint
    # print(transformedList)
    

loadData.to_file("./cla/sum/bxy_afterc3.geojson", driver='GeoJSON', encoding="GB2312")
# print(loadData.GetProjiection())