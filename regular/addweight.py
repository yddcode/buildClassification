import cv2

ori_img = cv2.imread('D:/111/Rectangle_05_Level_18.tif', 1)

mask = cv2.imread('labels5cont.png', 1)

add = cv2.addWeighted(ori_img, 0.5, mask, 0.5, 0.1)
cv2.imwrite('labels5add.png', add)