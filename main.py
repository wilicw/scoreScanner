from os import pread
import cv2
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.python.keras.backend import shape
from core.flat2grid import flat2grid
from core.pic2flat import pic2flat
from core.sepdigit import sepdigit
from nn.core import predict

img = cv2.imread("core/sct8.jpg")
flatImg = pic2flat(img).getFinal()
gridImg = flat2grid(flatImg).getFinal()

# digit = cv2.imread("core/digit.png", 0)
# for digit in sepdigit(digit).getFinal():
#     plt.imshow(digit, cmap="gray"), plt.show()
#     digit = digit.astype("float32") / 255
#     digit = np.expand_dims(digit, -1)
#     print(predict(digit))

resultCsv = ""

for index, box in enumerate(gridImg):
    # print(box[0], end=" ")
    if box[0][0] == 0:
        resultCsv += ","
    elif box[0][1] == 0:
        resultCsv += f"{box[0][0]},"
    else:
        # plt.imsave("digit.png", box[1], cmap="gray", format="png")
        digits = sepdigit(box[1]).getFinal()
        if len(digits) == 0:
            resultCsv += ","
        else:
            digitsStr = ""
            for digit in digits:
                # plt.imshow(digit, cmap="gray"), plt.show()
                digit = digit.astype("float32") / 255
                digit = np.expand_dims(digit, -1)
                predictResult = predict(digit)
                # if max(predictResult) < 0.55:
                #     digitsStr += "X"
                # else:
                digitsStr += str(np.argmax(predictResult))
            resultCsv += f"{digitsStr},"
    try:
        if box[0][1] > gridImg[index + 1][0][1]:
            resultCsv += "\n"
    except:
        resultCsv += "\n"

    # plt.imshow(box[1], cmap="gray"), plt.show()
    # print()

with open("result.csv", "w") as f:
    f.write(resultCsv)