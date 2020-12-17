import cv2
import numpy as np
from core.flat2grid import flat2grid
from core.pic2flat import pic2flat
from core.sepdigit import sepdigit
from nn.core import predict
from flask import Flask, jsonify, request, send_from_directory
from flask_restful import Api, Resource
from flask_cors import CORS
import uuid, os, threading

# from matplotlib import pyplot as plt
# from tensorflow.python.keras.backend import shape


def process(path, __uuid):
    i = 0
    img = cv2.imread(path)
    flatImg = pic2flat(img).getFinal()
    gridImg = flat2grid(flatImg).getFinal()

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
                    # cv2.imwrite(f"/tmp/{i}.png", digit)
                    # plt.imshow(digit, cmap="gray"), plt.show()
                    digit = digit.astype("float32") / 255
                    if 0.08 <= np.sum(digit) / 784 <= 0.75:
                        digit = np.expand_dims(digit, -1)
                        predictResult = predict(digit)
                        digitsStr += str(np.argmax(predictResult))
                    else:
                        digitsStr += ""
                    i += 1
                resultCsv += f"{digitsStr},"
        try:
            if box[0][1] > gridImg[index + 1][0][1]:
                resultCsv += "\n"
        except:
            resultCsv += "\n"
    with open(f"/tmp/{__uuid}.csv", "w") as f:
        f.write(resultCsv)


app = Flask(__name__)
CORS(app)
api = Api(app)


class uploadScoreTable(Resource):
    def get(self):
        return jsonify({"status": 200})

    def post(self):
        data = request.files["img"]
        __uuid = uuid.uuid4().hex
        path = f"/tmp/{__uuid}.png"
        data.save(path)
        _ = threading.Thread(target=process, args=(path, __uuid))
        _.start()
        return jsonify({"status": 200, "uuid": __uuid})


class getScoreTable(Resource):
    def get(self, _uuid):
        if _uuid.isalnum():
            if os.path.isfile(f"/tmp/{_uuid}.csv"):
                return send_from_directory("/tmp", f"{_uuid}.csv", as_attachment=True)
            else:
                return jsonify({"status": 404, "msg": "File not exist or not yet!"})
        else:
            return jsonify({"status": 418})


app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
api.add_resource(uploadScoreTable, "/api/upload/scoreTable")
api.add_resource(getScoreTable, "/api/get/scoreTable/<_uuid>", "/api/get/scoreTable")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
