import subprocess
import fileinput
import shutil
from skimage import io, util
import os


# saturation levels
colourRange = ['2', '2e-1', '2e-2', '2e-3', '2e-4']
# max modes to generate
maxMode = 6

# open template kat file
originalKat = open('cavity.kat', 'r')

# loop over m, then n, then colour range
for m in range(maxMode):
    for n in range(maxMode):
        for c in range(5):

                # generate names
                current = "cavity-"+str(m)+"-"+str(n)+"-"+colourRange[c]
                generateFileName = current+".kat"

                # make and/or change directory
                if not os.path.exists(current): os.mkdir(current)
                shutil.copy("cavity.kat", current+'/'+generateFileName)
                os.chdir(current)

                # generate new lines for .kat
                temLine = "tem laser "+str(m)+" "+str(n)+" 0.1 0.0" #replace lines
                colourLine = "set cbrange[0:"+colourRange[c]+"]"

                # replacing lines in .kat
                with fileinput.FileInput(generateFileName, inplace=True, backup='.bak') as file:
                        for line in file:
                            line = line.rstrip()
                            if "#replaceMode" in line:
                                line = line.replace("#replaceMode", temLine)
                            elif "#replaceColour" in line:
                                line = line.replace("#replaceColour", colourLine)
                            print(line)

                # run the new kat file
                subprocess.run(["../../finesse/./kat", generateFileName])

                #adding noise to generated image
                imageName = current+".png"
                noisyName = current+'-noise'+'.png'
                cavityImage = io.imread(imageName)
                noisyCavity = util.random_noise(cavityImage, mode='gaussian', clip=True)
                io.imsave(noisyName, noisyCavity)

                # cleaning files
                fileList = os.listdir()
                notImages = [x for x in fileList if not '.png' in x]
                for fileName in notImages: os.remove(fileName)

                #move back up directory
                os.chdir('..')
originalKat.close()
