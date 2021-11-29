from osgeo import gdal
from osgeo import osr
import numpy as np
import geopandas as gp

# Tiles_file = "C:\\Program Files (x86)\\BMDownload\\Rectangle_btiff_卫图\\Rectangle_btiff_卫图_Level_18.tif"
Tiles_file = 'cla/wanpian/newImg10.tif'

dataset = gdal.Open(Tiles_file) # 读入影像文件
nXSize,nYSize=dataset.RasterXSize,dataset.RasterYSize # 影像列数，行数

# 读取Shapefile文件./cla/Rectangle_1.shp
# loadData = gp.read_file("C:/Program Files (x86)/BMDownload/Rectangle_bwgs_建筑轮廓/Rectangle_bwgs_建筑轮廓.shp") # .dbf prj shap shx tdb
# print("读取的数据：", loadData)

# # 判断Shapefile文件的格式，有点、线、面三种
# loadType = loadData['geometry'][0].geom_type
# print("空间数据类型：", loadType)

trans = dataset.GetGeoTransform() 
prosrs = osr.SpatialReference()
prosrs.ImportFromWkt(dataset.GetProjection())
geosrs = prosrs.CloneGeogCS()

ct2 = osr.CoordinateTransformation(geosrs, prosrs)   # 表示从地理坐标系映射到投影坐标系

coords = ct2.TransformPoint(120.151514672788366, 30.185400361267686)  # 【经纬度坐标】

Pro_lon = coords[0]   # 【投影坐标】经度方向
Pro_lat = coords[1]  # 【投影坐标】纬度方向

trans = dataset.GetGeoTransform()

col_id = int((Pro_lon - trans[0]) / trans[1]+0.000000001)    # 【图像坐标】列方向 +0.000000001为了填补浮点数计算误差

row_id = int((trans[3] - Pro_lat ) / -trans[5]+0.000000001)  #【图像坐标】行方向  -trans[5] 为正数
print('图像坐标:', col_id, row_id)

a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
b = np.array([Pro_lon - trans[0], Pro_lat - trans[3]])
value =  np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解
print('图像坐标2:', value)