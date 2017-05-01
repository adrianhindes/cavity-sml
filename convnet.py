import numpy as np # Arrays
import matplotlib.pyplot as plt
import os # Navigating directories
from random import shuffle # Mixing up ordered data
from tqdm import tqdm
from PIL import Image
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

TRAINDIR = 'newData'
IMGSIZE = 128 # Pixels
learnRate = 1e-3 # Learning rate of neural network

# Keeping track of our convnet models
# We'll use TensorBoard to compare

MODELNAME = 'modeRecog-{}-{}.model'.format(learnRate, '2conv-basic')

# Maxmimum mode number to train and test for, 0 inclusive
modeNum = 6

trainSet = 'training.npy'

'''
Assuming data has already been generated from PyKat and Finesse, we now need to go ahead and add images to input features and labels arrays. 

First we define a function to obtain labels (mode numbers n,m) from file names, which are given by nm_0_random.png. Then we create training and testing data arrays, where the training array is a list of tuples, (imgdata,label), and training data (imgdata,identifier), where the identifier is the unique number from the Keras image modification preprocessing we did before.

We'll be using one-hot arrays, and for $n, m$ mode numbers, the array will be of size $nm$. The labels and output array will be of the encoded form [{00}, {01}, {02},...,{0m},{10},...,{nm}]

'''

# Get modes from a file name
def getModes(fileName):
    modes = fileName.split('_')[-3]
    n = int(modes[0])
    m = int(modes[1])
    array = np.zeros((modeNum,modeNum),dtype='int8')
    array[n,m] = 1
    label = np.ndarray.flatten(array)
    return label

# creating array to feed into network

def createDataArray(dataDirectory):
    # Start with an empty list
    dataList = []
    print('Generating data for '+dataDirectory)
 # For each image in given directory
    for img in tqdm(os.listdir(dataDirectory)):
        # Label for image
        label = getModes(img)
        # Actually load image
        img = Image.open(dataDirectory+img).convert('L')
        # Resize if necessary (commented out since already done in data generation)
        # img = img.resize((IMGSIZE,IMGSIZE))
        arr = np.array(img.getdata(), dtype=np.uint8)
        # Append image data with label
        dataList.append([arr,label])
    # Shuffle it around for good measure
    shuffle(dataList)
    name = dataDirectory.split('/')[1]
    # Save so we don't have to do this every time
    np.save(name+'.npy', dataList)
    return dataList

# Create training data. We will split this later for training and validation
if os.path.isfile(trainSet):
    trainData = np.load(trainSet)
else:
    trainData = createDataArray(TRAINDIR)

# Now create the convnet graph
convnet = input_data(shape=[None, IMGSIZE, IMGSIZE,1], name='input')

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 128, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, modeNum*modeNum, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=learnRate, loss='categorical_crossentropy', name='targets')


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
X = np.array([i[0] for i in train])
Y = [i[1] for i in train]

testingX = np.array([i[0] for i in test])
testingY = [i[1] for i in test]

# Fit the model!

model.fit({'input': X}, {'targets': Y}, n_epoch=2,
          validation_set=({'input': testingX}, {'targets': testingY}),
          snapshot_step=200, show_metric=True, run_id=MODELNAME)

