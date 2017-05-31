import numpy as np  # Arrays
import os  # Navigating directories
from random import shuffle  # Mixing up ordered data
from tqdm import tqdm  # Progress bars
import cv2  # Image manipulation
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import matplotlib.pyplot as plt
# Running Finesse
import subprocess
# Editing kat file
import fileinput
# Copying files
import shutil


FINESSEDIR = "../Finesse/./kat"

MODELNAME = 'modeRecog-0.001-final.model'
IMGSIZE = 128
modeNum = 6
learnRate = 1e-3
rawDataFolder = 'rawData'

# Open kat file
originalKat = open('cavity.kat', 'r')

# Convnet graph
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


def getLabel(fileName):
    # Assume clean filename "cavitynm.png"
    modes = fileName[6:8]
    n = int(modes[0])
    m = int(modes[1])
    array = np.zeros((modeNum, modeNum), dtype='int8')
    array[n, m] = 1
    label = np.ndarray.flatten(array)
    return label

def getMode(label):
    reshaped = label.reshape(6,6)
    location = np.where(reshaped == 1)
    n = (location[0])[0]
    m = (location[1])[0]
    return (n,m)

def createDataArray(dataDirectory):
    # Start with an empty list
    dataList = []
    print('Generating data for '+dataDirectory)
    # For each image in given directory
    for file in tqdm(os.listdir(dataDirectory)):

        # Label for image
        label = getLabel(file)

        # Actually load image
        img = cv2.imread(dataDirectory+'/'+file, cv2.IMREAD_GRAYSCALE)

        # Resize
        img = cv2.resize(img, (IMGSIZE, IMGSIZE))

        # Append image data with label
        dataList.append([np.array(img), label])
    # Save so we don't have to do this every time
    # Will be saved as (name of the folder).npy
    np.save(dataDirectory+'.npy', dataList)
    return dataList

if os.path.isfile(rawDataFolder+'.npy'):
    checkData = np.load(rawDataFolder+'.npy')
else:
    checkData = createDataArray(rawDataFolder)


# Checking raw data
results = []
for data in checkData:
    imgData = data[0]
    label = data[1]
    predLabel = predict(imgData)

    # label -> string
    mode = str(getMode(label))
    predMode = str(getMode(predLabel))
    results.append([imgData, mode, predMode])

# preview results

fig=plt.figure()
for num, data in enumerate(results[:6]):
    img = data[0]
    y = fig.add_subplot(3,4,num+1)
    y.imshow(imgData, cmap='gray')
    plt.title(data[2])
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)

plt.show()

# Loop


