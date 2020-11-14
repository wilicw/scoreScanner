import cv2
import numpy as np
from matplotlib import pyplot as plt


class pic2flat:
    def __init__(self, __img):
        self.img = __img
        self.__final = None
        self.__preprocess()
        self.__contoursprocess()

    def getFinal(self):
        return self.__final

    def __preprocess(self):
        self.__bw_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.__blur = cv2.GaussianBlur(self.__bw_img, (3, 3), 0)
        self.__final = None
        self.__shape = self.img.shape

    def __findEdge(self):
        edges = cv2.Canny(self.__blur, 0, 180)
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        hierarchy = hierarchy[0]
        location_point_7, location_point_5 = [], []
        for i in range(len(contours)):
            k = i
            c = 0
            while hierarchy[k][2] != -1:
                k = hierarchy[k][2]
                c = c + 1
            if c == 7:
                location_point_7.append(i)
            if c == 5:
                location_point_5.append(i)

        location_point_5 = sorted(
            location_point_5, key=lambda x: cv2.contourArea(contours[x])
        )[1:4]
        location_point_7 = sorted(
            location_point_7, key=lambda x: cv2.contourArea(contours[x])
        )[:1]

        location_box_5 = []
        for i in location_point_5:
            rect = cv2.minAreaRect(contours[i])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            box = list(map(np.array, box))
            location_box_5.append(box)
        location_box_7 = []
        for i in location_point_7:
            rect = cv2.minAreaRect(contours[i])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            box = list(map(np.array, box))
            location_box_7.append(box)
        return location_box_5, location_box_7

    def __contoursprocess(self):
        img_center = np.array([self.__shape[0] / 2, self.__shape[1] / 2], dtype="int32")
        l5_edge = []
        l7_edge = None
        location_box_5, location_box_7 = self.__findEdge()
        for box in location_box_5:
            index = np.array([np.linalg.norm(dot - img_center) for dot in box]).argmin()
            l5_edge.append(box[index])
        for box in location_box_7:
            index = np.array([np.linalg.norm(dot - img_center) for dot in box]).argmin()
            l7_edge = box[index]
        corner = sorted(
            l5_edge, key=lambda x: np.linalg.norm(np.array([x]) - np.array([l7_edge]))
        )
        pos = [1600, 2000]
        src = np.float32(
            [
                [corner[2][0], corner[2][1]],
                [corner[1][0], corner[1][1]],
                [corner[0][0], corner[0][1]],
                [l7_edge[0], l7_edge[1]],
            ]
        )
        dst = np.float32(
            [
                [500, 500],
                [500 + pos[0], 500],
                [500, 500 + pos[1]],
                [500 + pos[0], 500 + pos[1]],
            ]
        )
        M = cv2.getPerspectiveTransform(src, dst)
        cutImage = cv2.warpPerspective(self.img, M, (1000 + pos[1], 1000 + pos[1]))
        cut = 2
        self.__final = cutImage[
            500 + cut : 500 - cut + pos[1], 500 + cut : 500 - cut + pos[0]
        ]
        # plt.imshow(self.__final), plt.show()
