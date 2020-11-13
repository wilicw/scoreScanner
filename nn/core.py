from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
x_train = X_train.reshape(60000, 1, 28, 28) / 255
x_test = X_test.reshape(10000, 1, 28, 28) / 255
y_train = to_categorical(Y_train)
y_test = to_categorical(Y_test)

model = Sequential(
    Conv2D(
        filters=32,
        kernel_size=3,
        input_shape=(1, 28, 28),
        activation="relu",
        padding="same",
    ),
    MaxPool2D(pool_size=2, data_format="channels_first"),
    Flatten(),
    Dense(256, activation="relu"),
    Dense(10, activation="softmax"),
)

print(model.summary())
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(x_train, y_train, epochs=10, batch_size=64, verbose=1)