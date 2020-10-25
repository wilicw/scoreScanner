from itertools import count
import cv2
from matplotlib import container
import numpy as np
from matplotlib import pyplot as plt
import itertools
import imutils


img = cv2.imread("answer1.jpg")
blur = cv2.GaussianBlur(img, (3, 3), 0)
img1 = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

img = cv2.imread("answer3.jpg")
blur = cv2.GaussianBlur(img, (3, 3), 0)
img2 = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
detector = cv2.ORB_create()
kp1, des1 = detector.detectAndCompute(img1, None)
kp2, des2 = detector.detectAndCompute(img2, None)

matches = bf.match(des1, des2)

# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)

# Draw first 10 matches.
imMatches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None)
plt.imshow(imMatches), plt.show()
