import cv2
import numpy as np
import pyhht
import matplotlib.pyplot as plt
from pyhht.visualization import plot_imfs

image = cv2.imread("dan.jpg")
image = cv2.resize(image, (108, 108))

image2 = cv2.imread('images.jpg')
image2 = cv2.resize(image2, (108, 108))


pi = 3.14
temp = image.flatten()
temp2 = image2.flatten()
t = np.linspace(0, 1, 34992)
# modes = np.sin(2 * pi * 5 * t) + np.sin(2 * pi * 10 * t)
# x = modes + t
temp = temp + t
temp2 = temp2 + t

hilbert = pyhht.EMD(temp)
imfs = hilbert.decompose()

hilbert2 = pyhht.EMD(temp2)
imfs2 = hilbert.decompose()


print(imfs.shape, imfs2.shape)

plot_imfs(temp, imfs, t)
plot_imfs(temp, imfs2, t)
