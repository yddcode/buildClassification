import cv2, os

def checkImgMask(img, mask):

    img = cv2.imread(img)
    mask = cv2.imread(mask)

    cv2.imshow('img_', img)
    # cv2.imshow('mask_%s'%mask, mask)

    addw = cv2.addWeighted(img, 0.5, mask, 0.5, 0)
    cv2.imshow('addweighted', addw)
    cv2.waitKey(0)


if __name__ == "__main__":

    "检查原图和马赛克匹配情况"

    dir = './cla/test/'
    for filename in os.listdir(dir + 'img/'):
        if filename.endswith('jpg') or filename.endswith('tif'):
            print('filename:', filename)
            checkImgMask(dir + 'img/'+filename, dir + 'mask/'+filename)
            