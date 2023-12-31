# -*- coding: utf-8 -*-
"""TFbuildModelandTrain.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Vq6oS0gKmSpFxEZowpGWsDC97Xho7rHa

**建立資料**
"""

import tensorflow as tf

X = tf.constant([[1.0,2.0,3.0],[4.0,5.0,6.0]])
Y = tf.constant([[10.0],[20.0]])

"""**建模型**"""

class Linear(tf.keras.Model):
  def __init__(self):
    super().__init__()
    self.dense = tf.keras.layers.Dense(
        units=10000,
        activation=None,
        kernel_initializer=tf.zeros_initializer(),
        bias_initializer=tf.zeros_initializer()
    )

  def call(self,input):
    output = self.dense(input)
    return output

"""**運行**"""

model = Linear()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

for i in range(100):
  with tf.GradientTape() as tape:
    y_pred = model(X)
    loss = tf.reduce_sum(tf.square(y_pred - Y))
  grads = tape.gradient(loss,model.variables)
  optimizer.apply_gradients(grads_and_vars=zip(grads,model.variables))

  print(model.variables)