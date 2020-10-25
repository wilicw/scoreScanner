from itertools import groupby
from matplotlib.pyplot import grid
import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
from numpy.core.fromnumeric import shape
from numpy.core.records import array


def slope(x1, y1, x2, y2):
    return (y2-y1)/(x2-x1) if x2-x1 != 0 else np.inf


class flat2grid():
    def __init__(self, __img):
        self.img = __img
        self.__final = None
        self.__preprocess()
        self.__process()

    def getFinal(self):
        return self.__final

    def __preprocess(self):
        self.__bw_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(
            ~self.__bw_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
        rows, cols = binary.shape
        scale = 40
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilated_col = cv2.dilate(eroded, kernel, iterations=1)
        scale = 20
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilated_row = cv2.dilate(eroded, kernel, iterations=1)
        self.__outline = cv2.bitwise_or(dilated_col, dilated_row)
        self.__cross = cv2.bitwise_and(dilated_col, dilated_row)

    def __process(self):
        ys, xs = np.where(self.__cross > 0)
        x, y = [], []
        myxs = np.sort(xs)
        myys = np.sort(ys)
        i = 0
        for i in range(len(myxs)-1):
            if(myxs[i+1]-myxs[i] > 10):
                x.append(myxs[i])
            i = i+1
        x.append(myxs[i])

        for i in range(len(myys)-1):
            if(myys[i+1]-myys[i] > 10):
                y.append(myys[i])
            i = i+1
        y.append(myys[i])
        for i in range(len(y)-1):
            for j in range(len(x)-1):
                crop = cv2.rectangle(
                    self.img, (x[j], y[i]), (x[j+1], y[i+1]), (0, 0, 0), 2)
                # crop = self.img[y[i]:y[i+1], x[j]:x[j+1]]
        plt.imshow(self.img, cmap="gray"), plt.show()

    #   linesP = cv2.HoughLinesP(self.__outline, 1, np.pi / 180, 50, None, 50, 10)
    #   if linesP is not None:
    #     for i in range(0, len(linesP)):
    #       x1,y1,x2,y2 = linesP[i][0]
    #       print(slope(x1,y1,x2,y2))
    #       cv2.line(self.img, (x1,y1), (x2,y2), (0,0,255), 3, cv2.LINE_AA)
    #   plt.imshow(self.img, cmap="gray"),plt.show()
