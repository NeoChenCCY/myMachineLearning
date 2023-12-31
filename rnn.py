# -*- coding: utf-8 -*-
"""RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X7LAYbiJD4b86ILUra0nBcfCPBZnEiH7

**載入文字資料**
"""

import tensorflow as tf
import numpy as np

class DataLoader():
  def __init__(self):
    path = tf.keras.utils.get_file('nietzsche.txt',origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')

    with open(path,encoding='utf-8') as f:
      self.raw_text = f.read().lower()

    self.chars = sorted(list(set(self.raw_text)))
    self.char_indices = dict((c,i) for i, c in enumerate(self.chars))
    self.indices_char = dict((i,c) for i, c in enumerate(self.chars))
    self.text = [self.char_indices[c] for c in self.raw_text]

  def get_batch(self, seq_length, batch_size):
    seq = []
    next_char = []

    for i in range(batch_size):
      index = np.random.randint(0, len(self.text) - seq_length)
      seq.append(self.text[index:index+seq_length])
      next_char.append(self.text[index+seq_length])

      return np.array(seq), np.array(next_char)

"""**建立模型**"""

from numpy.core.multiarray import dtype
class RNN(tf.keras.Model):
  def __init__(self, num_chars, batch_size, seq_length):
    super().__init__()

    self.num_chars = num_chars
    self.seq_length = seq_length
    self.batch_size = batch_size

    self.cell = tf.keras.layers.LSTMCell(units=256)
    self.dense  = tf.keras.layers.Dense(units=self.num_chars)

  def call(self, inputs, from_logits=False):
    inputs = tf.one_hot(inputs, depth=self.num_chars)
    state = self.cell.get_initial_state(batch_size=self.batch_size,dtype=tf.float32)

    for t in range(self.seq_length):
      output, state = self.cell(inputs[:,t,:],state)

    logits = self.dense(output)

    if from_logits:
      return logits
    else:
      return tf.nn.softmax(logits)

"""**參數設定**"""

num_batches = 1000
seq_length = 40
batch_size = 1
learning_rate = 1e-3

""" **訓練開始**"""

from keras.engine.training import optimizer
data_loader = DataLoader()
model = RNN(num_chars=len(data_loader.chars),batch_size=batch_size,seq_length=seq_length)
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

for batch_index in range(num_batches):
  X, y = data_loader.get_batch(seq_length,batch_size)
  with tf.GradientTape() as tape:
    y_pred = model(X)
    loss = tf.keras.losses.sparse_categorical_crossentropy(y_true=y,y_pred=y_pred)
    loss = tf.reduce_mean(loss)
    print("batch %d loss %f" % (batch_index,loss.numpy()))
  grads = tape.gradient(loss,model.variables)
  optimizer.apply_gradients(grads_and_vars=zip(grads,model.variables))

"""**預測**"""

def predict(self, inputts,temperature=1.):
  batch_size, _ = tf.shape(inputs)
  logits = self(inputs, from_logits=True)
  prob = tf.nn.softmax(logits / temperature).numpy()

  return np.array([np.random.choice(self.num_chars,p=prob[i,:]) for i in range(batch_size.numpy())])

X_, _ = data_loader.get_batch(seq_length,1)

for diversity in [2,5,10,12]:
  X = X_
  print("diversity %f:" % diversity)
  data_loader.indices_char = {}
  for t in range(400):
    y_pred = model.predict(X,diversity)
    y_pred_tuple = tuple(y_pred[0])
    print(data_loader.indices_char[y_pred_tuple],end='',flush=True)
    X =np.concatenate([[X[:,1:]],np.expand_dims(y_pred,axis=1)],axis=-1)

  print("\n")

print(data_loader.chars)