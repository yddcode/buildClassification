from osgeo import gdal
from osgeo import osr
import numpy as np
 
def getSRSPair(dataset):
    '''
    获得给定数据的投影参考系和地理参考系
    :param dataset: GDAL地理数据
    :return: 投影参考系和地理参考系
    '''
    prosrs = osr.SpatialReference()
    prosrs.ImportFromWkt(dataset.GetProjection())
    geosrs = prosrs.CloneGeogCS()
    return prosrs, geosrs
 
def geo2lonlat(dataset, x, y):
    '''
    将投影坐标转为经纬度坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param x: 投影坐标x
    :param y: 投影坐标y
    :return: 投影坐标(x, y)对应的经纬度坐标(lon, lat)
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(prosrs, geosrs)
    coords = ct.TransformPoint(x, y)
    return coords[:2]
 
 
def lonlat2geo(dataset, lon, lat):
    '''
    将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param lon: 地理坐标lon经度
    :param lat: 地理坐标lat纬度
    :return: 经纬度坐标(lon, lat)对应的投影坐标
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(geosrs, prosrs)
    coords = ct.TransformPoint(lon, lat)
    return coords[:2]
 
def imagexy2geo(dataset, row, col):
    '''
    根据GDAL的六参数模型将影像图上坐标（行列号）转为投影坐标或地理坐标（根据具体数据的坐标系统转换）
    :param dataset: GDAL地理数据
    :param row: 像素的行号
    :param col: 像素的列号
    :return: 行列号(row, col)对应的投影坐标或地理坐标(x, y)
    '''
    trans = dataset.GetGeoTransform()
    px = trans[0] + col * trans[1] + row * trans[2]
    py = trans[3] + col * trans[4] + row * trans[5]
    return px, py
 
 
def geo2imagexy(dataset, x, y):
    '''
    根据GDAL的六 参数模型将给定的投影或地理坐标转为影像图上坐标（行列号）
    :param dataset: GDAL地理数据
    :param x: 投影或地理坐标x
    :param y: 投影或地理坐标y
    :return: 影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
    '''
    trans = dataset.GetGeoTransform()
    a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
    b = np.array([x - trans[0], y - trans[3]])
    return np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解
 
 
if __name__ == '__main__':
    gdal.AllRegister()
    # 影像左上角横坐标：geoTransform[0]
    # 影像左上角纵坐标：geoTransform[3]

    # 遥感图像的水平空间分辨率为geoTransform[1]
    # 遥感图像的垂直空间分辨率为geoTransform[5]
    # 通常geoTransform[5] 与 geoTransform[1]相等

    # 如果遥感影像方向没有发生旋转，即上北、下南，则
    # geoTransform[2] 与 row *geoTransform[4] 为零。

    dataset = gdal.Open('D:/111/Rectangle_taishun_train/Rectangle_train3_Level_18.tif')
    # dataset = gdal.Open('cla/wanpian/newImg10.tif')
    print('数据投影：仿射矩阵')
    print(dataset.GetProjection(), '\n', dataset.GetGeoTransform(), '\n', dataset.GetProjectionRef())
    print('数据的大小（行，列）：')
    print('(%s %s)' % (dataset.RasterYSize, dataset.RasterXSize))
 
    x = 120.119089803931573 # 464201 119.839092493057294, 27.49283053788529
    y = 30.30033985901278 # 5818760
    lon = 119.839092493057294 #122.47242
    lat = 27.49283053788529 #52.51778
    row = 5.384615384615384 #2399
    col = 410.0 #3751
 
    # print('投影坐标 -> 经纬度：')
    # coords = geo2lonlat(dataset, x, y)
    # print('(%s, %s)->(%s, %s)' % (x, y, coords[0], coords[1]))
    print('经纬度 -> 投影坐标：')
    coords = lonlat2geo(dataset, lat, lon)
    print('(%s, %s)->(%s, %s)' % (lon, lat, coords[0], coords[1]))
 
    # print('图上坐标 -> 投影坐标：')
    # coords = imagexy2geo(dataset, row, col)
    # print('(%s, %s)->(%s, %s)' % (row, col, coords[0], coords[1]))
    print('投影坐标 -> 图上坐标：')
    coords = geo2imagexy(dataset, coords[0], coords[1])
    print('(%s, %s)->(%s, %s)' % (x, y, coords[0], coords[1]))
