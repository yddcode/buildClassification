import cv2
from test import corp_margin

mask = cv2.imread('./cla/sum/maskb.jpg')

im = cv2.imread('./cla/sum/c3b.jpg')
# im = cv2.copyMakeBorder(im,351,351,300,325,cv2.BORDER_REPLICATE)
img_re, row_top, raw_down, col_top, col_down = corp_margin(im)

maskcut = mask[row_top:raw_down+1, col_top:col_down+1, :]
c3cut = im[row_top:raw_down+1, col_top:col_down+1, :]

cv2.imwrite('./cla/sum/maskcut.jpg', maskcut)
cv2.imwrite('./cla/sum/c3cut.jpg', c3cut)