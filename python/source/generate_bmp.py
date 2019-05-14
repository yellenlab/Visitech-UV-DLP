from PIL import Image
import numpy as np

def bmp_from_poslist(positions, name, path,
                     radius=20,
                     image_width=1920,
                     image_height=1080):
    ''' Generates a 1-bit .bmp file

    args:
        positions: a PositionList() of the locations 
                   to illuminate
        name: name of the file
        path: location to save the .bmp file
        radius: radius of illuminated point
        image_width: number of pixels
        image_height: number of pixels
    '''
    bmp = np.zeros((1080,1920))
    for posit in positions:
        for i in range(image_height):
            for j in range(image_width):
                if ((np.abs(i-posit.y) < radius) and
                    (np.abs(j-posit.x) < radius)):
                    bmp[i][j] = 255

    im = Image.fromarray(bmp)
    im = im.convert('1')
    im.save("your_file.bmp")
