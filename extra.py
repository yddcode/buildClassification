import cv2
import numpy as np  

#load image and convert to hsv
img = cv2.imread("./cla/1.png")

# draw gray box around image to detect edge buildings
h,w = img.shape[:2]
cv2.rectangle(img,(0,0),(w-1,h-1), (50,50,50),1)

# convert image to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# define color ranges
low_yellow = (0,28,0)
high_yellow = (27,255,255)

low_gray = (0,0,0)
high_gray = (179,255,233)

# create masks
yellow_mask = cv2.inRange(hsv, low_yellow, high_yellow )
gray_mask = cv2.inRange(hsv, low_gray, high_gray)

# combine masks
combined_mask = cv2.bitwise_or(yellow_mask, gray_mask)
kernel = np.ones((3,3), dtype=np.uint8)
combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_DILATE,kernel)

# findcontours
contours, hier = cv2.findContours(combined_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# find and draw buildings
for x in range(len(contours)):
    # if a contour has not contours inside of it, draw the shape filled
    c = hier[0][x][2]
    if c == -1:
        cv2.drawContours(img,[contours[x]],0,(0,0,255),-1)

# draw the outline of all contours
for cnt in contours:
    cv2.drawContours(img,[cnt],0,(0,255,0),2)

# display result
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()