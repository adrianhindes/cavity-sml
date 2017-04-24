# Take raw Finesse data
# Transform through rotations, shears, rescalings and flips to
# generate training and validation data sets

from keras.preprocessing.image import ImageDataGenerator, array_to_img, \
    img_to_array, load_img
from skimage import util, io
from PIL import Image
import os
from shutil import copyfile

# rotation range randomly rotates pictures (0-180)
# width/height_shift ranges (frac of total w/h) to randomly translate
# rescale multiplies data before other processing
# shear_range randomly applies shearing transforms
# zoom_range randomly zooms inside pictures
# horizontal flip does what it says
# fill mode fills newly created pixels, can appear after transforms
trainDatagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
testDatagen = ImageDataGenerator(
        rotation_range=25,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.3,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest')
#
#
maxMode = 6

dataFolder = 'rawData/'
ext = '.png'

os.chdir('rawData')
files = os.listdir()
imageList = [x for x in files if '.png' in x]
os.chdir('..')

possibleModes = [str(m)+str(n) for m in range(maxMode) for n in range(maxMode)]

# Create file structure if it does not exist
if not os.path.exists('newData'): os.mkdir('newData')
os.chdir('newData')
for mode in possibleModes:
    if not os.path.exists(mode): os.mkdir(mode)
os.chdir('..')

if not os.path.exists('training'): os.mkdir('training')
os.chdir('training')
for mode in possibleModes:
    if not os.path.exists(mode): os.mkdir(mode)

os.chdir('..')


# Generators which read pictures in subfolders of training and validation,
# indefinitely generate batches of augmented cavity images

print('Generating training data set')
for folder in possibleModes:
    filteredImages = [x for x in files if 'cavity'+folder in x]
    for image in filteredImages:
        loaded = load_img('rawData/'+image)
        array = img_to_array(loaded)
        array = array.reshape((1,)+array.shape)
        i = 0
        for batch in trainDatagen.flow(array, batch_size=1, save_to_dir='training/'+folder,
                                       save_prefix=folder, save_format='png'):
            i += 1
            if i > 10: break
        print('generated '+image+' set')

print('Generating validation data set')
for folder in possibleModes:
    filteredImages = [x for x in files if 'cavity'+folder in x]
    for image in filteredImages:
        loaded = load_img('rawData/'+image)
        array = img_to_array(loaded)
        array = array.reshape((1,)+array.shape)
        i = 0
        for batch in testDatagen.flow(array, batch_size=1, save_to_dir='validation/'+folder,
                                       save_prefix=folder, save_format='png'):
            i += 1
            if i > 10: break
        print('generated '+image+' set')


#Noisify folders
for folder in possibleModes:
    imagesTrain = os.listdir('training/'+folder)
    os.chdir('training/'+folder)
    for image in imagesTrain:
        loaded = io.imread(image)
        noisy = util.random_noise(loaded, mode='gaussian', clip=True)
        io.imsave(image, noisy)
    os.chdir('../../')
    imagesValidate = os.listdir('validation/'+folder)
    os.chdir('validation/'+folder)
    for image in imagesValidate:
        loaded = io.imread(image)
        noisy = util.random_noise(loaded, mode='gaussian', clip=True)
        io.imsave(image, noisy)
    os.chdir('../../')
    print('generated noise for '+folder)



    #    for noiseNum in range(2):
     #       noisyName = (image.rstrip(ext))+'-'+str(noiseNum)+'.png'
      #      noisyCavity1 = util.random_noise(cavityImage, mode='gaussian', clip=True, seed=(noiseNum+1))
       #     noisyCavity2 = util.random_noise(cavityImage, mode='gaussian', clip=True, seed=(noiseNum+5))
        #    io.imsave('training/'+mode+'/'+noisyName, noisyCavity1)
         #   io.imsave('validation/'+mode+'/'+noisyName, noisyCavity2)

