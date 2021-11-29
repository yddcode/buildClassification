import cv2
# 256 33 8448  8318 7936 h 130 65
# 256 41 10496 10461 9984 w 35 17 18
# 19057 9406 18432 8704   625 702 ./cla/sum/c3.jpg
img = cv2.imread('D:/111/Level_18.tif', 1)


# img = cv2.imread('./cla/1.jpg', 1)
# img = cv2.copyMakeBorder(img,351,351,300,325,cv2.BORDER_REPLICATE)
# cv2.imwrite('./cla/sum/c3b.jpg', img)
h, w, c = img.shape

mask = cv2.imread('cla/1test_building.jpg', 1)
# mask = mask[200:h-20, 50:w-400]
# b = cv2.copyMakeBorder(mask,60,160, 320,130, cv2.BORDER_CONSTANT,value=[0,0,0])
# cv2.imwrite('./cla/sum/maskb.jpg', b)

# maskre = cv2.imread('./cla/sum/maskb.jpg', 1)
maskre = mask
# maskre = cv2.resize(mask, (w, h))
# for i in range(h):
#     for j in range(w):
#         maskre[:,:,2][i][j] = 2

# cv2.namedWindow("maskre", 0)
# cv2.resizeWindow("maskre", 1000,800)
# cv2.imshow('maskre', maskre)
print(img.shape, mask.shape, maskre.shape)
# alpha 为第一张图片的透明度
alpha = 0.5
# beta 为第二张图片的透明度
beta = 0.5
gamma = 0
# cv2.addWeighted 将原始图片与 mask 融合
mask_img = cv2.addWeighted(img, alpha, maskre, beta, gamma)

cv2.imwrite('./cla/sum/mbi_mask.png', mask_img)
cv2.namedWindow("mask", 0)
cv2.resizeWindow("mask", 1000,800)
cv2.imshow('mask', mask_img)
cv2.waitKey(0)
