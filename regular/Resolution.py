import math, gdal
from geopy.distance import geodesic
from osgeo import gdal, osr
import numpy as np

def radi(d):
  return d * 3.1415926 / 180

def read_img(filename):
    dataset = gdal.Open(filename) #打开文件
    im_width = dataset.RasterXSize  #栅格矩阵的列数
    im_height = dataset.RasterYSize  #栅格矩阵的行数
    im_bands = dataset.RasterCount   #波段数
    im_geotrans = dataset.GetGeoTransform()  #仿射矩阵，左上角像素的大地坐标和像素分辨率
    im_proj = dataset.GetProjection() #地图投影信息，字符串表示
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)

    # del dataset 
    print(im_bands, im_height, im_width, im_geotrans, im_proj)

    return im_bands, im_data, dataset, im_height, im_width

def getDist(lat1, lat2, lon1, lon2):
    radlat = radi(lat1) - radi(lat2)
    radlon = radi(lon1) - radi(lon2)
    print(radlat, radlon)
    dist = 2*math.asin(math.sqrt(math.pow(math.sin(radlat/2), 2) + math.cos(radi(lat1)) * math.cos(radi(lat2))*math.pow(math.sin(radlon/2), 2))) #math.pow
    dist = math.floor(dist * 6378137 * 10000) / 10000
    return dist

def getDist2(lat1, lat2, lon1, lon2):
    # dist = geodesic((30.28708, 120.12802999999997), (28.7427, 115.86572000000001)).km  #
    dist = geodesic((lat1, lon1), (lat2, lon2))
    return dist

from math import sin, asin, cos, radians, fabs, sqrt
 
EARTH_RADIUS = 6371  # 地球平均半径，6371km

def hav(theta):
    s = sin(theta / 2)
    return s * s
 
def get_distance_hav(lat0, lng0, lat1, lng1):
    """用haversine公式计算球面两点间的距离。"""
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
 
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance

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

def resolu(filename):

    im_bands, im_data, dataset, im_height, im_width = read_img(filename)
    trans = dataset.GetGeoTransform()
    x0, y0, xResolution, yResolution = trans[0], trans[3], trans[1], trans[5]
    coords = geo2lonlat(dataset, x0, y0)
    print('(%s, %s)->(%s, %s)' % (trans[0], trans[3], coords[0], coords[1]))

    px, py = imagexy2geo(dataset, im_height, im_width)
    print('(%s, %s) -> (%s, %s)' %(im_height, im_width, px, py))
    y1, x1 = geo2lonlat(dataset, px, py)
    # y0, x0 = coords[0], coords[1]
    # y1 = y0 - yResolution * im_data.shape[1]
    y0 = coords[0]
    x0 = coords[1]
    # coords = geo2lonlat(dataset, x0, y1)
    print('(%s, %s)->(%s, %s)' % (x0, y1, coords[0], coords[1]))
    print(x0, y0, y1, xResolution, yResolution, im_data.shape)
    # y1 = coords[0]
    # print(y0, y1, x0, x0)
    ylength1 = getDist(y0, y1, x0, x0)
    
    
    xylength = getDist2(y0, y1, x0, x1)
    print('xylength, ylength1 :: ', xylength, ylength1)
    xyResolu, yResolu1 = xylength / math.sqrt(im_data.shape[1] ** 2 + im_data.shape[0] ** 2), ylength1 / im_data.shape[1]

    # x1 = x0 + xResolution * im_data.shape[2]
    xlength1 = getDist(y0, y0, x0, x1)
    xlength = getDist2(y0, y0, x0, x1)
    print(xlength, xlength1)
    xResolu, xResolu1 = xlength / im_data.shape[2], xlength1 / im_data.shape[2]
    print(xResolu, xResolu1, xyResolu, yResolu1)
    return xResolu1, yResolu1, xlength1, ylength1



if __name__ == '__main__':

    xResolu, yResolu, xlength, ylength = resolu('D:/111/Rectangle_03_卫图/Rectangle_03_卫图_Level_18.tif')
    print('xResolu, yResolu :: ', xResolu, yResolu, xlength, ylength)