import numpy as np
from scipy.special.orthogonal import hermite
from PIL import Image
# constants to start with
# copying wikipedia constants
# https://en.wikipedia.org/wiki/File:Hermite-gaussian.png

size = 320  # size of image in pixels
I_0 = 1.
w = size/4.  # relative width of gaussian mode

m = 2
n = 2

raw = Image.new('F', (size, size))


# loop over x and y to compute hermite-gauss values for each pixel

for x in range(1, size, 2):
    for y in range(1, size, 2):
        I = I_0 * (hermite(m)(np.sqrt(2)*x/w)*np.exp(-x**2/w**2))**2 \
            * (hermite(n)(np.sqrt(2)*y/w)*np.exp(-y**2/w**2))**2
        raw.putpixel((int((size/2+(x-1)/2)), int(size/2+(y-1)/2)), I)
        raw.putpixel((int((size/2+(x-1)/2)), int(size/2-(y+1)/2)), I)
        raw.putpixel((int((size/2-(x+1)/2)), int(size/2+(y-1)/2)), I)
        raw.putpixel((int((size/2-(x+1)/2)), int(size/2-(y+1)/2)), I)
        print("row", str((x+1)/2), "of", str(size/2), "complete")

# normalize and export to sRGB


def linear_to_sRGB(l):
    if l <= 0.00304:
        l = 12.92*l
    else:
        l = 1.055*np.power(l, 1.0/2.4) - 0.055
    return 255.0*l

cooked = Image.new('L', (size,size))

for x in range(size):
  for y in range(size):
    l = raw.getpixel((x,y))
    cooked.putdata((x,y), linear_to_sRGB(l))
cooked.save(("hermiteGauss-2-2.png"))
