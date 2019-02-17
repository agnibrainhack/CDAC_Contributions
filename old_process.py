import cv2
import numpy as np
import matplotlib.pyplot as plt
import operator
# import image


horizontal_trend = []
potential = []
new_pot = []
all_points_in_iter = []

final_set = []
set = []

def test(step = 800):
    horizontal_trend_0 = []
    for i in range(step):
        var = 600 - (np.count_nonzero(indicator_matrix[i, :]))
        if var != 0:
            horizontal_trend_0.append(var)

    # print(horizontal_trend_0)
    points = []
    for i in range(len(horizontal_trend_0)):
        if horizontal_trend_0[i] == 600:
            points.append(i)
    final_points = []
    final_points_rev = []
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



    #rev
    for i in range(0, length):

        try:
            if points[i + 1] - points[i] > 6:
                final_points_rev.append(points[i])
                break
        except:
            pass

    for i in range(length, 0, -1):
        try:
            if points[i] - points[i - 1] > 6:
                final_points_rev.append(points[i])


        except:
            pass




    final_points.sort()
    final_points_rev.sort()

    new_points = []
    #new_points= final_points + final_points_rev

    for i in range(0, len(final_points), 1):
        try:
            new_points.append(final_points[i])

            if final_points[i+1] < final_points_rev[i]:
                final_points.remove(final_points[i+1])
                # if final_points[i + 2] < final_points_rev[i]:
                #     final_points.remove(final_points[i + 2])
                #     if final_points[i + 3] < final_points_rev[i]:
                #         final_points.remove(final_points[i + 3])
            new_points.append(final_points_rev[i])
        except:
            break

    diff = 0
    times = 0
    for i in range(0, len(new_points) - 1):
        diff = diff + new_points[i + 1] - new_points[i]
        times = times + 1

    try:
        mean = diff / times
    except:
        ZeroDivisionError
        mean = 0

    # print(mean)
    added = []
    # final_points = np.asarray(final_points)



    return new_points, mean

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



image = cv2.imread("new_sample.png")
image = cv2.imread("sample.jpg")
image = cv2.resize(image, (800, 800))

image = cv2.bilateralFilter(image,1,55,55)

# grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# binary

ret, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
ret,thresh = cv2.threshold(thresh,160,255,cv2.THRESH_OTSU)
global m
m = []
size = []
# erode
for k in range(200, 1000, 200):

    for i in range(1, 13):
        kernel1 = np.ones((i, 3), np.uint8)
        img_erode = cv2.erode(thresh, kernel1, iterations=1)
        # ?cv2.imshow("new1", img_erode)
        # dilation
        # kernel2 = np.ones((1, 80), np.uint8)
        # img_dilation = cv2.dilate(img_erode, kernel2, iterations=1)

        indicator_matrix = img_erode[0:k, 0:600]
        #print(indicator_matrix)
        x, m1 = test(k)

        all_points_in_iter.append(x)
        m.append(m1)


    length_array = []
    for i in range(0, len(all_points_in_iter), 1):
        length_array.append(len(all_points_in_iter[i]))


    index, value = max(enumerate(length_array), key=operator.itemgetter(1))
    #print(value)
    set = all_points_in_iter[index]

    enter = True

    temp = 0
    #print(m[index])
    status = False


    # for i in range(0, len(set)-1):
    #
    #     value = find_mean(set)
    #     #print(value)
    #
    #     #print(i)
    #     try:
    #
    #         if set[i + 1] - set[i] < value and set[i + 2] - set[i + 1] < value:
    #             set.remove(set[i + 1])
    #             #i = i - 1
    #
    #
    #
    #     except IndexError:
    #         break

            #temp = value


    start = 1


    kernel1 = np.ones((13, 1), np.uint8)
    img_test = cv2.erode(thresh, kernel1, iterations=1)
    test_arr = img_test[0:k, 0:300]

    while status:

        #print(var_len)
        try:
            var_len = np.count_nonzero(test_arr[set[start], :])

            if var_len > 2:
                set.remove(set[start])
        except:
            status = False
        start = start + 1



    again_mean = find_mean(set)
    #final_set.append(set)
    status = True
    temp = 0


#
# for i in range(0, len(set)-1):
#
#     value = find_mean(set)
#     #print(value)
#
#     #print(i)
#     try:
#
#         if set[i + 1] - set[i] < 2 and set[i + 2] - set[i + 1] < 2:
#             set.remove(set[i + 1])
#             #i = i - 1
#
#
#
#     except IndexError:
#         pass


for i in range(0, len(set), 1):
    cv2.line(image, (0, set[i]), (800, set[i]), (0, 0, 255), 1)


cv2.imshow('final', image)
cv2.waitKey(0)



