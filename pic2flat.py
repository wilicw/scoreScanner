import cv2
import numpy as np
from matplotlib import pyplot as plt
import itertools


class pic2flat():
    def __init__(self, __img):
        self.img = __img
        self.__final = None
        self.__preprocess()
        self.__contoursprocess()

    def getFinal(self):
        return self.__final

    def __preprocess(self):
        self.__bw_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.__blur = cv2.GaussianBlur(self.__bw_img, (5, 5), 0)
        self.__final = None
        self.__shape = self.img.shape

    def __findEdge(self):
        edges = cv2.Canny(self.__blur, 0, 180)
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        hierarchy = hierarchy[0]
        found = []
        for i in range(len(contours)):
            k = i
            c = 0
            while hierarchy[k][2] != -1:
                k = hierarchy[k][2]
                c = c + 1
            if c >= 5:
                found.append(i)
        found = sorted(found, key=lambda x: cv2.contourArea(contours[x]))[:3]
        boxes = []
        for i in found:
            rect = cv2.minAreaRect(contours[i])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            box = list(map(np.array, box))
            boxes.append(box)
        return boxes

    def __contoursprocess(self):
        img_center = np.array(
            [self.__shape[0]/2, self.__shape[1]/2], dtype='int32')
        edge = []
        for box in self.__findEdge():
            index = np.array([np.linalg.norm(dot - img_center)
                              for dot in box]).argmin()
            edge.append(box[index])
        _ = list(itertools.combinations(edge, 2))
        cross = _[np.array([np.linalg.norm(i[0] - i[1]) for i in _]).argmax()]
        cross_line_middle = ((cross[1] + cross[0])/2).astype(int)
        corner = None
        for _ in edge:
            if not list(filter(lambda x: np.array_equal(x, _), cross)):
                corner = _
        pos = [800, 1000]
        src = np.float32([
            [corner[0], corner[1]],
            [cross[0][0], cross[0][1]],
            [cross[1][0], cross[1][1]]
        ])
        dst = np.float32([
            [500, 500],
            [500+pos[0], 500],
            [500, 500+pos[1]]
        ])
        M = cv2.getAffineTransform(src, dst)
        cutImage = cv2.warpAffine(self.img, M, (1000+pos[1], 1000+pos[1]))
        self.__final = cutImage[495: 505+pos[1], 495:505+pos[0]]
