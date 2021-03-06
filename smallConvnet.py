import numpy as np  # Arrays
import os  # Navigating directories
from random import shuffle  # Mixing up ordered data
from tqdm import tqdm  # Progress bars
import cv2  # Image manipulation
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

TRAINDIR = 'newData'
IMGSIZE = 128  # Pixels
learnRate = 1e-3  # Learning rate of neural network

# Keeping track of our convnet models
# We'll use TensorBoard to compare

MODELNAME = 'smallModes-{}-{}.model'.format(learnRate, '')

# Maxmimum mode number to train and test for, 0 inclusive
modeNum = 2

trainSet = 'small'+TRAINDIR+'.npy'

'''
Assuming data has already been generated from PyKat and Finesse,
we now need to go ahead and add images to
input features and labels arrays.

First we define a function to obtain labels (mode numbers n,m)
from file names, which are given by nm_0_random.png.
Then we create training and testing data arrays,
where the training array is a list of tuples,
(imgdata,label), and training data (imgdata,identifier),
where the identifier is the unique number from
the Keras image modification preprocessing we did before.

We'll be using one-hot arrays, and for $n, m$ mode numbers,
the array will be of size $nm$.
The labels and output array will be of the encoded form
[{00}, {01}, {02},...,{0m},{10},...,{nm}]

'''

# Get modes from a file name


def getModes(fileName):
    modes = fileName.split('_')[-3]
    n = int(modes[0])
    m = int(modes[1])
    array = np.zeros((modeNum, modeNum), dtype='int8')
    array[n, m] = 1
    label = np.ndarray.flatten(array)
    return label

# creating array to feed into network


def createDataArray(dataDirectory):
    # Start with an empty list
    dataList = []
    print('Generating data for '+dataDirectory)
    # For each image in given directory
    files = os.listdir(dataDirectory)
    possibleModes = [str(m)+str(n) for m in range(modeNum) for n in range(modeNum)]
    filteredFiles = [x for x in files if (x.split('_')[-3]) in possibleModes ]
    for file in tqdm(filteredFiles, ascii=True):

        # Label for image
        label = getModes(file)

        # Actually load image
        img = cv2.imread(dataDirectory+'/'+file, cv2.IMREAD_GRAYSCALE)

        # Resize
        img = cv2.resize(img, (IMGSIZE, IMGSIZE))

        # Append image data with label
        dataList.append([np.array(img), label])

    # Shuffle it around for good measure
    shuffle(dataList)
    # Save so we don't have to do this every time
    # Will be saved as (name of the folder).npy
    np.save(trainSet, dataList)
    return dataList


# Create training data. We will split this later for training and validation

if os.path.isfile(trainSet):
    trainData = np.load(trainSet)
else:
    trainData = createDataArray(TRAINDIR)

# Now create the convnet graph

convnet = input_data(shape=[None, IMGSIZE, IMGSIZE, 1], name='input')

convnet = conv_2d(convnet, 16, 64, activation='relu', trainable=True)
convnet = max_pool_2d(convnet, 16)
convnet = conv_2d(convnet, 16, 32, activation='relu', trainable=True)
convnet = max_pool_2d(convnet, 32)
convnet = conv_2d(convnet, 64, 8, activation='relu', trainable=True)
convnet = max_pool_2d(convnet,5)

convnet = conv_2d(convnet, 512, 8, activation='relu', trainable=True)
convnet = max_pool_2d(convnet, 5)

onvnet = conv_2d(convnet, 512, 8, activation='relu', trainable=True)
convnet = max_pool_2d(convnet, 5)

onvnet = conv_2d(convnet, 512, 8, activation='relu', trainable=True)
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 512, 8, activation='relu', trainable=True)
convnet = max_pool_2d(convnet, 5)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.5)

convnet = fully_connected(convnet, modeNum*modeNum, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=learnRate,
                     loss='categorical_crossentropy', name='targets')


model = tflearn.DNN(convnet, tensorboard_dir='log')

# we might run this file several times for different training scenarios,
# so saving the model every time, and loading it from previous runs
if os.path.exists('{}.meta'.format(MODELNAME)):
    model.load(MODELNAME)
    print('model loaded!')

# split data array into training and testing sets
dataLength = len(trainData)
half = int(round(dataLength/2.))

train = trainData[:-half]
test = trainData[-half:]

# Reshaping arrays before feeding network


X = np.array([i[0] for i in train]).reshape(-1, IMGSIZE, IMGSIZE, 1)
Y = [i[1] for i in train]

testingX = np.array([i[0] for i in test]).reshape(-1, IMGSIZE, IMGSIZE, 1)
testingY = [i[1] for i in test]

# Fit the model!

model.fit({'input': X}, {'targets': Y}, n_epoch=200,
          validation_set=({'input': testingX}, {'targets': testingY}),
          snapshot_step=200, show_metric=True, run_id=MODELNAME)
