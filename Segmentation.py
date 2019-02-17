import cv2
import numpy as np
import matplotlib.pyplot as plt
#import image
horizontal_trend = []
potential = []
new_pot = []
image = cv2.imread("sample.jpg")
image = cv2.resize(image, (800, 800))
#cv2.imshow('orig',image)
#cv2.waitKey(0)

#grayscale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray',gray)
# cv2.waitKey(0)

#binary
ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
#cv2.imshow('second',thresh)
#cv2.waitKey(0)

#dilation
kernel = np.ones((2, 3), np.uint8)
img_dilation = cv2.erode(thresh, kernel, iterations=1)
indicator_matrix = img_dilation[0:800, 0:300]
for i in range(800):
    var = (np.count_nonzero(indicator_matrix[i, :]))
    if var != 0:
        horizontal_trend.append(var)

print(horizontal_trend)
# min = np.argmin(horizontal_trend)
# print(min)

for i in range(0, len(horizontal_trend)):
    if abs(horizontal_trend[i] - 8) < 5:
        potential.append(i)

lineThickness = 1
length = len(potential)
print(length)
for i in range(length):
    if (potential[i] - potential[i - 1]) > 3:
        new_pot.append(potential[i])
#print(potential)
for i in range(0, len(new_pot), 1):

    cv2.line(img_dilation, (0, new_pot[i]), (800, new_pot[i]), (255, 255, 255), lineThickness)

cv2.imshow('dilated', img_dilation)


plt.plot(horizontal_trend)
plt.show()
cv2.waitKey(0)


def local_min(ys):
    return [y for i, y in enumerate(ys)
            if ((i == 0) or (ys[i - 1] >= y))
            and ((i == len(ys) - 1) or (y < ys[i+1]))]


#find contours
# im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# #sort contours
# sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
#
# for i, ctr in enumerate(sorted_ctrs):
#     # Get bounding box
#     x, y, w, h = cv2.boundingRect(ctr)
#     # Getting ROI
#     roi = image[y:y + h, x:x + w]
#
#     # show ROI
#     cv2.imshow('segment no:' + str(i), roi)
#     cv2.rectangle(image, (x, y), (x + w, y + h), (90, 0, 255), 2)
#     cv2.waitKey(0)
#
# cv2.imshow('marked areas', image)
# cv2.waitKey(0)