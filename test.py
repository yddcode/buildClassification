import cv2


# for i in range(h):
#     for j in range(w):
#         if imggray[i][j] == 255:
            # print('1')
        
# from skimage import io
# 304 8143 496 10079 10496 8448  417  305
def corp_margin(img):
    img2 = img.sum(axis = 2)
    (row,col) = img2.shape
    row_top = 0
    raw_down = 0
    col_top = 0
    col_down = 0
    for r in range(0,row):
        if img2.sum(axis=1)[r] < 700*col:
            row_top=r
            break

    for r in range(row-1,0,-1):
        if img2.sum(axis=1)[r] < 700*col:
            raw_down=r
            break

    for c in range(0,col):
        if img2.sum(axis=0)[c] < 700*row:
            col_top=c
            break

    for c in range(col-1,0,-1):
        if img2.sum(axis=0)[c] < 700*row:
            col_down=c
            break

    new_img = img[row_top:raw_down+1, col_top:col_down+1, :]
    print(row_top, raw_down, col_top, col_down)
    return new_img, row_top, raw_down, col_top, col_down

def imgflip(image):
    img0 = cv2.flip(image, 0)
    img1 = cv2.flip(image, 1)
    return img0, img1

if __name__=='__main__':
    # 去图像白边
    # im = cv2.imread('./cla/sum/cuiyuan_mask.jpg')
    # img_re, row_top, raw_down, col_top, col_down = corp_margin(im)
    # print(img_re.shape, im.shape)
    # io.imsave('result.png',img_re)
    # cv2.imshow('imgcut', img_re)
    # cv2.imwrite('./cla/22.jpg', img_re)
    # temp = 
    # im0, im1 = imgflip(im)
    # cv2.imwrite('./cla/sum/cuiyuan_mask.jpg', im0)

    im0 = cv2.imread('D:/data/BDCI2017-seg/CCF-training/1.png',1)
    im1 = cv2.imread('D:/data/BDCI2017-seg/CCF-training/1_class.png',1)
    im1 = im1 * 51
    print(im1.shape,im1[:10,200:203])
    cv2.namedWindow("im0", 0)
    cv2.resizeWindow("im0", 1000,800)
    cv2.imshow('im0', im0)
    cv2.namedWindow("im1", 0)
    cv2.resizeWindow("im1", 1000,800)
    cv2.imshow('im1', im1)
    cv2.waitKey(0)