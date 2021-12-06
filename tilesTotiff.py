import os, cv2, subprocess
import numpy as np
from osgeo import osr, gdal
from numpy.core.defchararray import count
from skimage.io import imread, imsave
imwrite = imsave

def createNewimg(dir):
  rows, cols = [], []
  for parent, dirname, filenames in os.walk(dir):
    # rows.append(len(filenames))
    # print(max(rows), min(rows))

    cols.append(len(dirname))
    # print('cols:', cols, max(cols))
    for filename in filenames:
      
      if filename.endswith('png'):
        # print(filename, os.path.basename(filename))
        index = filename.find(".", 0)  # 找到点号的位置
        ob = filename[index - 2:index]
        # print(ob, int(ob))  # 截取目标字符
        rows.append(int(ob))
        # print(os.path.basename(filename) + " " + filename[index - 1:index])  # 测试目标字符串
      # print(max(rows), min(rows))
  return max(cols), min(rows), max(rows)      

def pasteImg(dir, newImg, h1):  # opencv
  colIndex = 0
  for parent, dirname, filenames in os.walk(dir):
    print(parent, dirname)
    for filename in filenames:
      
      if filename.endswith('png'):
        index = filename.find(".", 0)  # 找到点号的位置
        ob = int(filename[index - 2:index])
        # img = cv2.imread(parent +'/'+ filename, 1)
        img = imread(parent +'/'+ filename, False)
        # print((ob-h1)*256, (ob-h1+1)*256, colIndex, (colIndex+256))
        newImg[(ob-h1)*256:(ob-h1+1)*256, colIndex-256:colIndex, :] = img
    colIndex += 256
  return newImg

def pasteImg(dir, newImg, h1):  # skimage
  colIndex = 0
  dirnames = []
  for parent, dirname, filenames in os.walk(dir):
    if dirname != None:

      # dirnames.append(dirname)
      dirname.sort()
    print(parent, dirname)
    for filename in filenames:
      
      if filename.endswith('png'):
        index = filename.find(".", 0)  # 找到点号的位置
        ob = int(filename[index - 2:index])
        # img = cv2.imread(parent +'/'+ filename, 1)
        img = imread(parent +'/'+ filename, False)
        # print((ob-h1)*256, (ob-h1+1)*256, colIndex, (colIndex+256))
        newImg[(ob-h1)*256:(ob-h1+1)*256, colIndex-256:colIndex, :] = img
    colIndex += 256
  return newImg

import math
def num2deg(xtile, ytile, zoom):
    # 瓦片编码转经纬坐标
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def radi(d):
  return d * 3.1415926 / 180

def getDist(lat1, lat2, lon1, lon2): # 计算pitch距离
    radlat = radi(lat1) - radi(lat2)
    radlon = radi(lon1) - radi(lon2)
    print(radlat, radlon)
    dist = 2*math.asin(math.sqrt(math.pow(math.sin(radlat/2), 2) + math.cos(radi(lat1)) * math.cos(radi(lat2))*math.pow(math.sin(radlon/2), 2))) #math.pow
    dist = math.floor(dist * 6378137 * 10000) / 10000
    return dist

def pitch512(dir, parent, dirname, filenames):
    # 4张瓦片拼一块
    dirnames = []
    nullimg = np.zeros((256,256,3), np.uint8)
    nullimg = 255 + nullimg
    pitchimgs = []
    lons = []

    basenum = int(os.path.basename(parent))
    dirtwo = dir+str(basenum+1)
    if os.path.exists(dirtwo): 
      
      print(len(os.listdir(dirtwo)))
      filenames = os.listdir(dirtwo)
      print(parent, dirname, filenames)
      # for filename in filenames:
      for i in range(0,len(os.listdir(dirtwo))-1,2):
          print(i)
        # if filename.endswith('png'):
          filename = filenames[i]
          index = filename.find(".", 0)  # 找到点号的位置
          # print(index, filename[index])
          
          num = int(filename[:index])
          lons.append(num)
          # lons.append(num+1)
          if os.path.exists(parent +'/'+ filename):
            img1 = imread(parent +'/'+ filename, False)
          else: img1 = nullimg
          if os.path.exists(parent +'/'+ str(num+1)+'.png'): 
            img2 = imread(parent +'/'+ str(num+1)+'.png', False)
          else: img2 = nullimg
          if os.path.exists(dir+str(basenum+1) +'/'+ filename):
            img3 = imread(dir+str(basenum+1) +'/'+ filename, False)
          else: img3 = nullimg
          if os.path.exists(dir+str(basenum+1) +'/'+ str(num+1)+'.png'):
            img4 = imread(dir+str(basenum+1) +'/'+ str(num+1)+'.png', False)
          else: img4 = nullimg

          pitchimg = np.zeros((512,512,3), np.uint8)
          pitchimg[:256, :256] = img1
          pitchimg[:256, 256:512] = img3
          pitchimg[256:512, :256] = img2
          pitchimg[256:512, 256:512] = img4
          pitchimgs.append(pitchimg)
    return pitchimgs, lons

# 赋值地理信息
def assign_spatial_reference_byfile(src_path, dst_path):
    src_ds = gdal.Open(src_path, gdal.GA_ReadOnly)
    sr = osr.SpatialReference()
    sr.ImportFromWkt(src_ds.GetProjectionRef())
    geoTransform = src_ds.GetGeoTransform()
    dst_ds = gdal.Open(dst_path, gdal.GA_Update)
    dst_ds.SetProjection(sr.ExportToWkt())
    dst_ds.SetGeoTransform(geoTransform)
    dst_ds = None
    src_ds = None
    print('', sr, geoTransform, sr.ExportToWkt())

#  保存tif文件函数
def writeTiff(im_data, im_geotrans, im_proj, path):
    print('shape :: ', im_data.shape)
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_height, im_width, im_bands = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape

    #创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if(dataset!= None):
        dataset.SetGeoTransform(im_geotrans) #写入仿射变换参数
        dataset.SetProjection(im_proj) #写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i+1).WriteArray(im_data[i])
    del dataset

def set_reference(img, spatial, lon, lat):
  # 依据图像左上右下经纬度坐标和投影信息保存为geotiff
  projection = ["""PROJCS["WGS 84 / Pseudo-Mercator",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Mercator_1SP"],PARAMETER["central_meridian",0],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +nadgrids=@null +wktext +no_defs"]]""", """GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]"""]

  path = './01.tif'

  geotrans = (lon, spatial, 0.0, lat, 0.0, -spatial)

  writeTiff(img, geotrans, projection[0], path)
  
  # return setimg

if __name__ == "__main__":

  dir = 'D:/111/wuyanlin_test/Tiles_BIGEMAP/18/'
  # dir = 'E:/浙江省/浙江省_卫图/Tiles_BIGEMAP/10/'
  # w, h1, h2 = createNewimg(dir)
  # print(w, h1, h2)
  # newImg = np.zeros(((h2-h1+1)*256, w*256, 3), np.uint8)
  # newImg = 255 + newImg
  # print(newImg.shape)

  # newImg = pasteImg(dir, newImg, h1)
  lat, lon = num2deg(218193, 110053, 18)  
  print(lat, lon)
  count = 0
  for parent, dirname, filenames in os.walk(dir):
      
      # print(parent, dirname)
      if dirname != []:
        lats = dirname
      if dirname == []:

        # dirnames.append(dirname)
        dirname.sort()
        basedir = parent
        hang = len(dirname)
        count += 1
        if count %2 == 1:
          print(lats)
          
          pitchImages, lons = pitch512(dir, parent, dirname, filenames)
          for i in range(len(pitchImages)):
            print(lons, lons[i], lats[count-1])
            lat, lon = num2deg(int(lats[count-1]), int(lons[i]), 18)
            print(lat, lon)

            lat2, lon2 = num2deg(int(lats[count-1])+1, int(lons[i])+1, 18)

            dist = getDist(lat, lat2, lon, lon2)
            distlon = getDist(lat, lat, lon, lon2)
            distlat = getDist(lat, lat2, lon, lon)
            print(dist, dist/math.sqrt(256*256), distlat/256, distlon/256)
            set_reference(np.array(pitchImages[i]), distlat/256, lon, lat)
            
            subprocess.call (["rastervision", "predict", "/opt/data/output/bundle/model-bundle.zip", "./01.tif", "prediction"],shell=True)
            cv2.imshow('pitch', np.array(pitchImages[i]))
            cv2.waitKey(0)
  # cv2.namedWindow("newImage",0)
  # cv2.resizeWindow("newImage", 1700, 1900) # 限定显示图像的大小
  # cv2.imshow('newImage', newImg)
  # imwrite('cla/wanpian/newImg10.tif', newImg)
  
  cv2.waitKey(0)
# os.system("python predict.py")
  # python -m rastervision.pipeline.cli run_command /opt/data/output/pipeline-config.json predict
  # rastervision predict /opt/data/output/bundle/model-bundle.zip /opt/src/data/Rectangle_xihu_Level_18.tif prediction

