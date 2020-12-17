import numpy as np
import cv2
from matplotlib import pyplot as plt
from numpy.core.fromnumeric import sort


class sepdigit:
    def __init__(self, __img):
        self.img = __img.copy()
        self.__final = None
        self.__process()

    def getFinal(self):
        return self.__final

    def __process(self):
        self.__final = []
        contours, hierarchy = cv2.findContours(
            self.img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        digits = []
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if w * h < 20:
                continue
            im = self.img[y : y + h, x : x + w]
            try:
                height, width = im.shape[0], im.shape[1]
                width_new = 28
                height_new = 28
                if width / height >= width_new / height_new:
                    im = cv2.resize(im, (width_new, int(height * width_new / width)))
                else:
                    im = cv2.resize(im, (int(width * height_new / height), height_new))
                f = np.zeros((28, 28), np.uint8)
                ax, ay = (28 - im.shape[1]) // 2, (28 - im.shape[0]) // 2
                f[ay : im.shape[0] + ay, ax : ax + im.shape[1]] = im
                digits.append([x, f])
            except Exception as e:
                print(e)
                continue
        for d in sorted(digits, key=lambda x: x[0]):
            self.__final.append(d[1])
