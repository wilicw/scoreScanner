import cv2
from matplotlib import pyplot as plt
from flat2grid import flat2grid
from pic2flat import pic2flat

img = cv2.imread("sct8.jpg")
flatImg = pic2flat(img).getFinal()
girdImg = flat2grid(flatImg).getFinal()
