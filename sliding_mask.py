# import the necessary packages
import time

from helpers import pyramid, sliding_window
from skimage.transform import pyramid_gaussian
import argparse
import cv2
import pyhht
import numpy as np
from skimage import io, color, img_as_ubyte
from skimage.feature import greycomatrix, greycoprops



# construct the argument parser and parse the arguments
hog = cv2.HOGDescriptor()



# load the image
image = cv2.imread('sample.jpg')
image = cv2.resize(image, (800, 1000))
(winW, winH) = (128, 128)

# loop over the image pyramid
for resized in pyramid(image, scale=1.5):
    # loop over the sliding window for each layer of the pyramid
    for (x, y, window) in sliding_window(resized, stepSize=32, windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue

        # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
        # MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
        # WINDOW
        #

        # since we do not have a classifier, we'll just draw the window
        clone = resized.copy()

        cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 0, 255), 2)

        sub_img = clone[y - 7:y + winH + 7, x - 7:x + winH + 7]
        #h = hog.compute(sub_img)
        if sub_img.shape[1] != 0 and sub_img.shape[0] != 0:
            h = hog.compute(sub_img)
            #print(h)

            grayImg = img_as_ubyte(color.rgb2gray(sub_img))

            distances = [1, 2, 3]
            angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
            properties = ['energy', 'homogeneity']

            glcm = greycomatrix(grayImg,
                                distances=distances,
                                angles=angles,
                                symmetric=True,
                                normed=True)

            feats = np.hstack([greycoprops(glcm, prop).ravel() for prop in properties])
            print(feats)
            with open('output.txt','a') as file:
                np.savetxt(file, feats, delimiter= ',')

            cv2.imshow("Window", sub_img)


        cv2.imshow("Window2", clone)
        cv2.waitKey(1)
        time.sleep(0.025)