# -*- coding: utf-8 -*-
"""TFAPI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OCN70P20TY2NXv9AvnkB0jJbZBd7oEgI
"""

import numpy as np
class MNISTLoader():
  def __init__(self):
    mnist = tf.keras.datasets.mnist
    (self.train_data,self.trainn_label),(self.test_data,self.test_label) = mnist.load_data()
    #mnist = tf.keras.datasets.mnist
    #(training_images, training_labels), (test_images, test_labels) = mnist.load_data()

    self.train_data = np.expand_dims(self.train_data.astype(np.float32) / 255.0,axis = -1)
    self.test_data = np.expand_dims(self.test_data.astype(np.float32) / 255.0,axis = -1)
    self.train_label = self.trainn_label.astype(np.int32)
    self.test_label = self.test_label.astype(np.int32)

    self.num_train_data, self.num_test_data = self.train_data.shape[0], self.test_data.shape[0]

  def get_batch(self, batch_size):
    index = np.random.randint(0, np.shape(self.train_data)[0], batch_size)

    return self.train_data[index,:], self.trainn_label[index]

import tensorflow as tf
moel = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100,activation=tf.nn.relu),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Softmax()

])

from keras.api._v2.keras import Input
inputs = tf.keras.Input(shape=(28,28,1))
x = tf.keras.layers.Flatten()(inputs)
x = tf.keras.layers.Dense(units=100,activation=tf.nn.relu)(x)
x = tf.keras.layers.Dense(units=10)(x)
outputs = tf.keras.layers.Softmax()(x)

model = tf.keras.Model(inputs=inputs,outputs=outputs)

import keras
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss = tf.keras.losses.sparse_categorical_crossentropy,
    metrics=[tf.keras.metrics.sparse_categorical_accuracy]
)

data_loader = MNISTLoader()
#參數
num_epochs = 5
batch_size = 50
learning_rate = 0.001
model.fit(data_loader.train_data, data_loader.train_label,epochs=num_epochs,batch_size=batch_size)

print(model.evaluate(data_loader.test_data,data_loader.test_label))

"""**儲存模型數值**
tf.saved_model.save(model, '/path/to/save/model')

**載入模型數據**
loaded_model = tf.saved_model.load('/path/to/saved/model')
"""