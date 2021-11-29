import cv2
import numpy as np

def CutToDataset(img, mask):

    imgs, masks = [], []
    for i in range(int(img.shape[0]/512)):
        for j in range(int(img.shape[1]/512)):
            ig = img[i*512:(i+1)*512, j*512:(j+1)*512]
            ma = mask[i*512:(i+1)*512, j*512:(j+1)*512]
            # cv2.imshow('img', ig)
            # cv2.imshow('ma', ma)
            # cv2.waitKey(0)
            imgs.append(ig)
            masks.append(ma)
    imgs, masks = np.array(imgs), np.array(masks)
    return imgs, masks

if __name__=='__main__':

    "生成数据集"

    dir = './cla/'
    img = cv2.imread(dir + 'sum/c3cut.jpg')
    mask = cv2.imread(dir + 'sum/maskcut.jpg')

    a, b = CutToDataset(img, mask)

    for i in range(len(a)):
        # print(i)
        cv2.imwrite(dir + 'test/img/h2_%d.jpg'%i, a[i])
        cv2.imwrite(dir + 'test/mask/h2_%d.jpg'%i, b[i])
    