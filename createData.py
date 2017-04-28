# Running Finesse
import subprocess
# Editing kat file
import fileinput
# Copying files
import shutil
# Adding Gaussian noise
from skimage import io, util
# Navigating directories
import os
# Cropping raw images
from PIL import Image
# Nice loading bars for loops
from tqdm import tqdm
# Keras preprocessing package for augmentation
from keras.preprocessing.image import ImageDataGenerator, array_to_img, \
    img_to_array, load_img


'''
Simple python script to generate data from Finesse
First we run Finesse iterated over mode numbers, m, n
(Just pure modes, no superpositions)
Fix up the GNUplot raw image
Then use Keras preprocessing package to generate modified data
(rotated, skewed, zoomed)
Then we add noise (after Keras, otherwise wacky things happen)
Ready to feed into neural network
'''

FINESSEDIR = "../Finesse/./kat"
# saturation levels
colourRange = ['2', '2e-1', '2e-2', '2e-3', '2e-4']
colourName = ['0', '1', '2', '3', '4']
# max mode for n and m to generate
maxMode = 6
# open template kat file
originalKat = open('cavity.kat', 'r')

# Define data folders
dataFolder = 'rawData'
newDataFolder = 'newData'

# Image extension
ext = '.png'

# No. images to generate per raw image
imageNum = 20


# loop over m, then n, then colour range
for m in tqdm(range(maxMode)):
    for n in range(maxMode):
        for c in range(5):

                # generate names
                current = "cavity"+str(m)+str(n)+colourName[c]
                generateFileName = current+".kat"

                # make and/or change directory
                if not os.path.exists(dataFolder): os.mkdir(dataFolder)
                shutil.copy("cavity.kat", dataFolder+'/'+generateFileName)
                os.chdir(dataFolder)

                # generate new lines for .kat
                temLine = "tem laser "+str(m)+" "+str(n)+" 0.1 0.0" #replace lines
                colourLine = "set cbrange[0:"+colourRange[c]+"]"

                # replacing lines in .kat
                file = fileinput.FileInput(generateFileName, inplace=True, backup='.bak')
                for line in file:
                    line = line.rstrip()
                    if "#replaceMode" in line:
                        line = line.replace("#replaceMode", temLine)
                    elif "#replaceColour" in line:
                        line = line.replace("#replaceColour", colourLine)
                    print(line)
                file.close()

                # run the new kat file
                subprocess.call(['../'+FINESSEDIR, generateFileName])

                # crop generated image
                # GNUplot generates a margin for some reason
                # assume square image
                image = Image.open(current+ext)
                width = image.size[0]
                height = width
                offset = height-1
                cropped = image.crop((width-offset, height-offset, width, height))
                cropped.save(current+ext)

                # cleaning files
                fileList = os.listdir()
                notImages = [x for x in fileList if not ext in x]
                for fileName in notImages: os.remove(fileName)

                #move back up directory
                os.chdir('..')

originalKat.close()

# Preprocessing
# Data generators, using Keras
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
files = os.listdir(dataFolder)
imageList = [x for x in files if '.png' in x]

possibleModes = [str(m)+str(n) for m in range(maxMode) for n in range(maxMode)]

# Create file structure if it does not exist
if not os.path.exists(newDataFolder): os.mkdir(newDataFolder)

# Generators which read pictures in subfolders of training and validation,
# indefinitely generate batches of augmented cavity images

print('Preprocessing raw data set')
for mode in tqdm(possibleModes):
       for image in [x for x in files if 'cavity'+mode in x]:
        loaded = load_img('rawData/'+image)
        array = img_to_array(loaded)
        array = array.reshape((1,)+array.shape)
        i = 0
        for batch in trainDatagen.flow(array, batch_size=1, save_to_dir=newDataFolder,
                                       save_prefix=mode, save_format=ext):
            i += 1
            if i > imageNum: break
        print('generated '+image+' set')

# Adding noise
def noisy(img):
    noisy = util.random_noise(loaded, mode='gaussian', clip=True)
    return noisy

for image in tqdm(newDataFolder):
    loaded = io.imread(newDataFolder+'/'+image)
    io.imsave(image, noisy(image))
