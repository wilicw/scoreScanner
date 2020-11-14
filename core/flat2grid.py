from itertools import groupby
from matplotlib.pyplot import box, grid
import numpy as np
import cv2
from matplotlib import pyplot as plt
from numpy.core.multiarray import result_type
from skimage import measure


class flat2grid:
    def __init__(self, __img):
        self.img = __img.copy()
        self.__final = None
        self.__preprocess()
        self.__process()

    def getFinal(self):
        return self.__final

    def __preprocess(self):
        self.__bw_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.__shape = self.__bw_img.shape
        # cv2.rectangle(self.__bw_img, (0, 0), (800, 1000), (0, 0, 0), 3)
        binary = cv2.adaptiveThreshold(
            ~self.__bw_img,
            10,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            35,
            -5,
        )
        rows, cols = self.__shape
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
        dots = [(5, 5)]
        labels, num = measure.label(
            self.__cross, connectivity=2, background=0, return_num=True
        )
        for i in range(1, num + 1):
            x, y = np.where(labels == i)
            dots.append(
                tuple(reversed(np.asarray(np.dstack((x, y))[0], dtype=int)[0].tolist()))
            )
        boxes = []

        def slope(x, y):
            dy = y[0] - x[0]
            dx = y[1] - x[1]
            return np.inf() if dx == 0 else dy / dx

        while len(dots) != 0:
            start = dots[0]
            end = sorted(
                list(
                    filter(
                        lambda x: (x[0] - start[0] > 0)
                        and (x[1] - start[1] > 0)
                        and (0.5 < slope(start, x) < 10),
                        dots,
                    )
                ),
                key=lambda x: np.linalg.norm(np.array([x]) - np.array([start])),
            )
            if len(end) != 0:
                end = end[0]
                boxes.append([start, end])
            dots.remove(start)
        tableBox = []
        for box in boxes:
            if (
                np.linalg.norm(
                    np.array([box[0][0], box[0][1]]) - np.array([box[1][0], box[1][1]])
                )
                < 25
            ):
                continue
            # cv2.rectangle(
            #     self.img,
            #     (box[0][0], box[0][1]),
            #     (box[1][0], box[1][1]),
            #     (255, 0, 0),
            #     1,
            # )
            margin = 5
            crop = self.img[
                box[0][1] + margin : box[1][1] - margin // 2,
                box[0][0] + margin : box[1][0] - margin // 2,
            ]
            ret, thresh1 = cv2.threshold(crop, 150, 255, cv2.THRESH_BINARY_INV)
            tableBox.append([thresh1, box[0]])
            # print(box[0], box[1])
            # plt.imshow(thresh1, cmap="gray"), plt.show()
        h = 50
        margin = 5
        sortedBox = []
        for i in range(40):
            hboxes = filter(
                lambda x: (i * h - margin < x[1][1] < (i + 1) * h - margin), tableBox
            )
            for index, box in enumerate(sorted(hboxes, key=lambda x: x[1][0])):
                sortedBox.append(((i, index), box[0]))
        for box in sortedBox:
            print(box[0])
            plt.imshow(box[1], cmap="gray"), plt.show()
        self.__final = sortedBox
