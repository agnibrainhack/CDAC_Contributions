import cv2
import numpy as np
import operator
# import image


horizontal_trend = []
potential = []
new_pot = []
all_points_in_iter = []


def test():
    horizontal_trend_0 = []
    for i in range(800):
        var = 600 - (np.count_nonzero(indicator_matrix[i, :]))
        if var != 0:
            horizontal_trend_0.append(var)

    # print(horizontal_trend_0)
    points = []
    for i in range(len(horizontal_trend_0)):
        if horizontal_trend_0[i] == 600:
            points.append(i)
    final_points = []
    length = len(points)
    total = 0
    for i in range(0, length):

        try:
            if points[i + 1] - points[i] > 6:
                final_points.append(points[i])
        except:
            pass

    for i in range(length, 0, -1):
        try:
            if points[i] - points[i - 1] > 6:
                final_points.append(points[i])
                break
        except:
            pass



    diff = 0
    times = 0
    for i in range(0, len(final_points) - 1):
        diff = diff + final_points[i + 1] - final_points[i]
        times = times + 1

    try:
        mean = diff / times
    except:
        ZeroDivisionError
        mean = 0

    # print(mean)
    added = []
    # final_points = np.asarray(final_points)

    new_points = final_points

    return new_points, mean




#img = cv2.imread('new_sample.png', 0)
image = cv2.imread('sample.jpg', 0)
img = cv2.resize(image, (800, 800))
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

kernel2 = np.ones((1, 1), np.uint8)
img_dilation = cv2.dilate(skel, kernel2, iterations=1)

cv2.imshow("skel", img_dilation)
cv2.waitKey(0)
cv2.destroyAllWindows()


global m
m = []
size = []
# erode
for i in range(1, 25):
    kernel1 = np.ones((i, 3), np.uint8)
    img_erode = cv2.erode(skel, kernel1, iterations=1)
    # ?cv2.imshow("new1", img_erode)
    # dilation
    # kernel2 = np.ones((1, 80), np.uint8)
    # img_dilation = cv2.dilate(img_erode, kernel2, iterations=1)

    indicator_matrix = img_erode[0:800, 0:600]
    #print(indicator_matrix)
    x, m1 = test()

    all_points_in_iter.append(x)
    m.append(m1)

set = []
length_array = []
for i in range(0, len(all_points_in_iter), 1):
    length_array.append(len(all_points_in_iter[i]))


index, value = max(enumerate(length_array), key=operator.itemgetter(1))
#print(value)
set = all_points_in_iter[index]



enter = True
i = 0

def find_mean(itr):
    diff = 0
    times = 0
    for i in range(0, len(itr) - 1):
        diff = diff + itr[i + 1] - itr[i]
        times = times + 1

    try:
        mean = diff / times
    except:
        ZeroDivisionError
        mean = 0
    return mean



temp = 0
#print(m[index])
status = False
for j in range(1, 10):
    while enter:

        value = find_mean(set)

        if value - temp > 5:

            try:
                if set[i+1] - set[i] < value and set[i+2] - set[i+1] < value:
                    set.remove(set[i+1])
                else:
                    i = i + 1
            except:
                enter = False
        else:
            status = True
            break

        temp = value
    if status:
        break

#print(set)
status = True
start = 1


kernel1 = np.ones((13, 1), np.uint8)
img_test = cv2.erode(skel, kernel1, iterations=1)
test_arr = img_test[0:800, 0:300]

while status:

    #print(var_len)
    try:
        var_len = np.count_nonzero(test_arr[set[start], :])

        if var_len > 5:
            set.remove(set[start])
    except:
        status = False
    start = start + 1


again_mean = find_mean(set)

status = True
i = 0
# while status:
#     try:
#         if set[i + 1] - set[i] < again_mean:
#             set.remove(set[i])
#         else:
#             i = i + 1
#     except:
#         status = False


for i in range(0, len(set), 1):
    cv2.line(image, (0, set[i]), (800, set[i]), (0, 0, 255), 1)


cv2.imshow('final', image)
cv2.waitKey(0)
