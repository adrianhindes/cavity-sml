import numpy as np  # Arrays
import os  # Navigating directories
from random import shuffle  # Mixing up ordered data
from tqdm import tqdm  # Progress bars
import cv2  # Image manipulation
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression


MODELNAME = 'modeRecog-0.001-final.model'
IMGSIZE = 128
modeNum = 6
learnRate = 1e-3

convnet = input_data(shape=[None, IMGSIZE, IMGSIZE, 1], name='input')
convnet = conv_2d(convnet, 30, 5, activation='relu')
convnet = max_pool_2d(convnet,2)
convnet = conv_2d(convnet, 30, 5, activation='relu')
convnet = max_pool_2d(convnet,2)
convnet = conv_2d(convnet, 30, 5, activation='relu')
convnet = max_pool_2d(convnet,2)
convnet = conv_2d(convnet, 30, 5, activation='relu')
convnet = max_pool_2d(convnet,2)
convnet = conv_2d(convnet, 30, 5, activation='relu')
convnet = max_pool_2d(convnet,2)
convnet = conv_2d(convnet, 30, 5, activation='relu')
convnet = max_pool_2d(convnet,2)
convnet = conv_2d(convnet, 30, 5, activation='relu')
convnet = max_pool_2d(convnet,2)
convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet,0.1)

convnet = fully_connected(convnet, modeNum*modeNum, activation='softmax')
convnet = regression(convnet, optimizer='momentum', learning_rate=learnRate,
                     loss='categorical_crossentropy', name='targets')


model = tflearn.DNN(convnet, tensorboard_dir='log')


if os.path.exists('{}.meta'.format(MODELNAME)):
    model.load(MODELNAME)
    print('model loaded!')
else:
    print('no model with given name')


def predict(img):
    img = cv2.resize(img, (IMGSIZE, IMGSIZE))
    input = img.reshape(IMGSIZE, IMGSIZE, 1)
    prediction = model.predict(input)
    return prediction


