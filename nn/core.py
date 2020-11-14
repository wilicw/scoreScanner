import os
from tensorflow.keras.models import load_model
import numpy as np

model_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mnist_cnn.h5")
model = load_model(model_file)


def predict(img):
    return model.predict(np.array([img]))[0]
