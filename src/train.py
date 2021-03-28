#!/usr/bin/env python

"""
Trains a simple cnn on the fashion mnist dataset.
Designed to show how to do a simple wandb integration with keras.
Also demonstrates resumption of interrupted runs with
    python train.py --resume
"""
import sys

from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Dense, Flatten
import tensorflow.keras.utils as np_utils
from tensorflow.keras.optimizers import SGD

import wandb
from wandb.keras import WandbCallback


defaults = dict(
    dropout=0.2,
    hidden_layer_size=128,
    layer_1_size=16,
    layer_2_size=32,
    learn_rate=0.01,
    decay=1e-6,
    momentum=0.9,
    epochs=27,
    )

resume = sys.argv[-1] == "--resume"
wandb.init(config=defaults, resume=resume)
config = wandb.config

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
labels = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
          "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

img_width, img_height = 28, 28

X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.

# reshape input data -- add channel dimension
X_train = X_train.reshape(X_train.shape[0], img_width, img_height, 1)
X_test = X_test.reshape(X_test.shape[0], img_width, img_height, 1)

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

sgd = SGD(lr=config.learn_rate, decay=config.decay, momentum=config.momentum,
          nesterov=True)

# build model
if wandb.run.resumed:
    print("RESUMING")
    # restore the best model
    model = load_model(wandb.restore("model-best.h5").name)
else:
    model = Sequential()
    model.add(Conv2D(config.layer_1_size, (5, 5), activation='relu',
                     input_shape=(img_width, img_height, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(config.layer_2_size, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(config.dropout))
    model.add(Flatten())
    model.add(Dense(config.hidden_layer_size, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(
        loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(X_train, y_train,  validation_data=(X_test, y_test),
          epochs=config.epochs,
          initial_epoch=wandb.run.step,  # for resumed runs
          callbacks=[WandbCallback(data_type="image", labels=labels)])

model.save("cnn.h5")