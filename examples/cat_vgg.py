import os
GPU = True

if GPU:
    os.environ['TNN_GPU'] = "True"

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

import pickle

import sys
sys.path.insert(1, "/content/tinynet/")

from tinynet.losses import cross_entropy_with_softmax_loss
from tinynet.learner import Learner
from tinynet.optims import SGDOptimizer
from tinynet.core import Backend as np
from tinynet.models.vgg16 import model

# Higher verbose level = more detailed logging
import tinynet

tinynet.utilities.logger.VERBOSE = 1



print('loading data...')
# mnist.init()

# Utilities
def load_data(filepath):
  with open(filepath, 'rb') as f:
    cat_dog_data = pickle.load(f)
    data = cat_dog_data['image']
    label = cat_dog_data['labels']
    x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=0.10, random_state=42)
    return x_train, y_train, x_test, y_test

def get_accuracy(y_predict, y_true):
    return np.mean(np.equal(np.argmax(y_predict, axis=-1),
                            np.argmax(y_true, axis=-1)))

x_train, y_train, x_test, y_test = load_data('dataset/cat_and_dog.pkl')

def preprocess_y(y_train, y_test):
  enc = OneHotEncoder(sparse=False, categories='auto')
  y_train = enc.fit_transform(y_train.reshape(len(y_train), -1))
  y_test = enc.transform(y_test.reshape(len(y_test), -1))
  return y_train, y_test

y_train, y_test = preprocess_y(y_train, y_test)

print(y_train.shape)
print(x_train.shape)

if GPU:
    import cupy as cp
    x_train = cp.array(x_train)
    y_train = cp.array(y_train)
    x_test = cp.array(x_test)
    y_test = cp.array(y_test)
    
model.summary()

learner = Learner(model, cross_entropy_with_softmax_loss,
                  SGDOptimizer(lr=0.01))

TRAIN = False

print('starting training...')

if TRAIN:
  learner.fit(x_train, y_train, epochs=5, batch_size=1)

  model.export('cat_and_dog.tnn')

else:
  model.load('cat_and_dog.tnn')

print('starting evaluating...')

y_predict = learner.predict(x_test, batch_size=1)

acc = get_accuracy(y_predict, y_test)
print('Testing Accuracy: {}%'.format(acc*100))