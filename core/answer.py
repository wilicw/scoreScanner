from itertools import count
import cv2
from matplotlib import container
import numpy as np
from matplotlib import pyplot as plt
import itertools
import imutils


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


class answer2text():
    def __init__(self, __img):
        self.img = __img
        self.__preprocess()
        self.__findEdge()
        # self.__contoursprocess()

    def getFinal(self):
        return self.__final

    def __preprocess(self):
        self.__blur = cv2.GaussianBlur(self.img, (5, 5), 0)
        self.__bw_img = cv2.cvtColor(self.__blur, cv2.COLOR_BGR2GRAY)
        self.__final = None
        self.__shape = self.img.shape

    def __findEdge(self):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        detector = cv2.SIFT_create()
        kps = detector.detect(self.__bw_img)
        print("# of keypoints: {}".format(len(kps)))
        # return
        # max_brightness = 0
        # edges = cv2.Canny(self.__blur, 30, 200)
        # src = self.__bw_img
        # contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        # (x, y, w, h) = cv2.boundingRect(contour)
        # self.__final = self.img[y:y+h, x:x+w]
        # shape = self.__final.shape
        # account = self.__final[0:int(shape[0]*58/312),]
        # isDead = self.__final[int(shape[0]*58/312):int(shape[0]*67/312),]
        # answer = self.__final[int(shape[0]*65/312):,]
        # # plt.imshow(answer)
        # plt.show()
        # for i in range(35):
        #   plt.imshow(answer[int(answer.shape[0]*i/35):int(answer.shape[0]*(i+1)/35),])
        #   plt.show()


img = cv2.imread("answer1.jpg")
pf = answer2text(img)
plt.imshow(pf.getFinal(), cmap="gray")
plt.title('Original Image')
plt.show()
