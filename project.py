# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 15:51:56 2017

@author: mohse
"""


import numpy as np
from skimage import data
from skimage.feature import canny
from scipy import ndimage as ndi
from skimage.filters import sobel
from skimage.morphology import watershed
from scipy.misc import toimage
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import colorsys
from scipy.misc import toimage
from scipy.ndimage import filters

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


image = Image.open('road.jpg')
imageArray = np.array(image)

gray_image = image.convert('L')
#gray_image.show()

hsv_image = image.convert('HSV')
#hsv_image.show()

hsvlist = []
for rgb in list(image.getdata()) :
# rgb is color at each pixel
    rval = rgb[0]/255.
    gval = rgb[1]/255.
    bval = rgb[2]/255.
    h, s, v = colorsys.rgb_to_hsv(rval, gval, bval)
    hsv = (int(h*255.), int(s*255.), int(v*255.))
    hsvlist.append(hsv)
img_hsv = Image.new(image.mode, image.size)
img_hsv.putdata(hsvlist)
#img_hsv.show()


lower_yellow = np.array([20, 100, 100], dtype = 'uint8')
upper_yellow = np.array([30, 255, 255], dtype= 'uint8')

mask_yellow = cv2.inRange(np.array(img_hsv), lower_yellow, upper_yellow)
mask_white = cv2.inRange(np.array(gray_image), 200, 255)
mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
mask_yw_image = cv2.bitwise_and(np.array(gray_image), mask_yw)