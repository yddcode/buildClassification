import cv2
import numpy as np

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

temp = cv2.imread('D:/111/Rectangle_taishun_train/Rectangle_train3_Level_18.tif', 1)
# temps = cv2.flip(temp, 1)
tempc = cv2.flip(temp, 0)
h, w = temp.shape[:2]
# M = cv2.getRotationMatrix2D((w // 2, h // 2), 90, 1.0)
# rotated = cv2.warpAffine(tempc, M, (w, h))
rotated = rotate_bound(tempc, 90)
cv2.imwrite('D:/111/Rectangle_taishun_train/Rectangle_train3_Level_18flip.tif', rotated)

 
from osgeo import osr, gdal
 
 
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
    
src_path = 'D:/111/Rectangle_taishun_train/Rectangle_train3_Level_18.tif'
# dst_path = 'cla/wanpian/newImg10.tif' # 
dst_path = 'D:/111/Rectangle_taishun_train/Rectangle_train3_Level_18flip.tif'
assign_spatial_reference_byfile(src_path, dst_path)