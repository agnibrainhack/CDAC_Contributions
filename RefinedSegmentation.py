import cv2
import numpy as np
import matplotlib.pyplot as plt

horizontal_trend_0 = []
horizontal_trend_1 = []
potential = []
new_pot = []
image = cv2.imread("dan.jpg")
image = cv2.resize(image, (800, 800))

#grayscale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#binary
ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)

#dilation
kernel = np.ones((1, 2), np.uint8)
img_dilation = cv2.erode(thresh, kernel, iterations=1)
indicator_matrix = img_dilation[0:800, 0:800]

for i in range(800):
    var = 300 - (np.count_nonzero(indicator_matrix[i, :]))
    if var != 0:
        horizontal_trend_0.append(var)
        horizontal_trend_1.append(300-var)
#horizontal_trend = np.asarray(horizontal_trend)

global_maximas_0 = []
global_maximas_1 = []
# print(horizontal_trend_0)
# print(horizontal_trend_1)

first_stage = True

for i in range(0, len(horizontal_trend_0) - 2, 1):
    #global_maximas_0.append()
    if first_stage and horizontal_trend_0[i + 1] - horizontal_trend_0[i] > 1:
        global_maximas_0.append(i)
        first_stage = False

    if not first_stage and horizontal_trend_0[i + 1] - horizontal_trend_0[i] > 1 and horizontal_trend_0[i + 1] - horizontal_trend_0[i + 2] > 1:

        if horizontal_trend_0[i + 1] - horizontal_trend_0[i - 1] > 3 and horizontal_trend_0[i + 1] - horizontal_trend_0[i + 3] > 3:

            global_maximas_0.append(i)

for i in range(len(horizontal_trend_0)-1, 1, -1):
    if horizontal_trend_0[i-1] - horizontal_trend_0[i] > 1:
        global_maximas_0.append(i)
        print(i)
        break

for i in range(0, len(horizontal_trend_1) - 2, 1):

    if horizontal_trend_1[i + 1] - horizontal_trend_1[i] > 3 and horizontal_trend_1[i + 1] - horizontal_trend_1[i + 2] > 3:

        if horizontal_trend_1[i + 1] - horizontal_trend_1[i - 1] > 5 and horizontal_trend_1[i + 1] - horizontal_trend_1[i + 3] > 5:

            global_maximas_1.append(i)


print(global_maximas_0)
print(global_maximas_1)



total = 0
length = len(global_maximas_0)
for i in range(1, length):
    total = total + (global_maximas_0[i] - global_maximas_0[i-1])
mean = total / length
print(mean)
t = 0
for i in range(0, len(global_maximas_1), 1):
    t = t + mean
    cv2.line(img_dilation, (0, global_maximas_1[i]), (300, global_maximas_1[i]), (255, 255, 255), 1)

cv2.imshow('dilated', img_dilation)
cv2.waitKey(0)



