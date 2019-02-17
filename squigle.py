import cv2
import numpy as np

image = cv2.imread('new_sample.png', 0)
#img = cv2.imread('sample.jpg', 0)
image = cv2.resize(image, (800, 800))
img = image
size = np.size(img)
skel = np.zeros(img.shape, np.uint8)

ret, img = cv2.threshold(img, 127, 255, 0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
done = False

while (not done):
    eroded = cv2.erode(img, element)
    temp = cv2.dilate(eroded, element)
    temp = cv2.subtract(img, temp)
    skel = cv2.bitwise_or(skel, temp)
    img = eroded.copy()

    zeros = size - cv2.countNonZero(img)
    if zeros == size:
        done = True

kernel1 = np.ones((2, 1), np.uint8)
img_test = cv2.erode(skel, kernel1, iterations=1)

horizontal_trend_0 = []
indicator_matrix = img_test[0:800, 0:600]
for i in range(800):
    var = 600 - (np.count_nonzero(indicator_matrix[i, :]))
    if var != 0:
        horizontal_trend_0.append(var)

points = []
for i in range(len(horizontal_trend_0)):
    if horizontal_trend_0[i] == 600:
        points.append(i)

for i in range(0, len(points), 1):
    cv2.line(image, (0, points[i]), (800, points[i]), (0, 0, 255), 1)


cv2.imshow("skel", image)
cv2.waitKey(0)
cv2.destroyAllWindows()