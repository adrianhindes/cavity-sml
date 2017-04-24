import subprocess
import fileinput
import shutil
from skimage import io, util
import os
from PIL import Image


# saturation levels
colourRange = ['2', '2e-1', '2e-2', '2e-3', '2e-4']
colourName = ['0', '1', '2', '3', '4']
# max modes to generate
maxMode = 6
# open template kat file
originalKat = open('cavity.kat', 'r')

# loop over m, then n, then colour range
for m in range(maxMode):
    for n in range(maxMode):
        for c in range(5):

                # generate names
                current = "cavity"+str(m)+str(n)+colourName[c]
                generateFileName = current+".kat"

                # make and/or change directory
                if not os.path.exists('rawData'): os.mkdir('rawData')
                shutil.copy("cavity.kat", 'rawData/'+generateFileName)
                os.chdir('rawData')

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

                # crop generated image
                # GNUplot generates a margin for some reason
                # assume square image
                image = Image.open(current+'.png')
                width = image.size[0]
                height = width
                offset = height-1
                cropped = image.crop((width-offset, height-offset, width, height))
                cropped.save(current+'.png')

                # cleaning files
                fileList = os.listdir()
                notImages = [x for x in fileList if not '.png' in x]
                for fileName in notImages: os.remove(fileName)

                #move back up directory
                os.chdir('..')

originalKat.close()
