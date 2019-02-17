import cv2
import numpy as np
import operator



horizontal_trend = []
potential = []
new_pot = []
all_points_in_iter = []
all_points_in_iter_rev = []
final_set = []
set = []
set_rev = []


def test(step = 800):
    horizontal_trend_0 = []
    for i in range(step):
        var = 600 - (np.count_nonzero(indicator_matrix[i, :]))
        if var != 0:
            horizontal_trend_0.append(var)
    points = []
    for i in range(len(horizontal_trend_0)):
        if horizontal_trend_0[i] == 600:
            points.append(i)
    final_points = []
    final_points_rev = []
    length = len(points)

    for i in range(0, length):

        try:
            if points[i + 1] - points[i] > 3:
                final_points.append(points[i])

        except:
            pass

    for i in range(length, 0, -1):
        try:
            if points[i] - points[i - 1] > 3:
                final_points.append(points[i])
                break

        except:
            pass


    #rev
    for i in range(0, length):

        try:
            if points[i + 1] - points[i] > 3:
                final_points_rev.append(points[i])
                break
        except:
            pass

    for i in range(length, 0, -1):
        try:
            if points[i] - points[i - 1] > 3:
                final_points_rev.append(points[i])
        except:
            pass




    final_points.sort()
    final_points_rev.sort()

    return final_points, final_points_rev

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
# image = cv2.imread("images.jpg")
# image = cv2.imread("sample.jpg")
image = cv2.resize(image, (800, 800))

image = cv2.bilateralFilter(image,1,55,55)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
ret,thresh = cv2.threshold(thresh,160,255,cv2.THRESH_OTSU)

# size = np.size(thresh)
# skel = np.zeros(thresh.shape, np.uint8)
#
# element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
# done = False
#
# img = thresh
# while (not done):
#     eroded = cv2.erode(img, element)
#     temp = cv2.dilate(eroded, element)
#     temp = cv2.subtract(img, temp)
#     skel = cv2.bitwise_or(skel, temp)
#     img = eroded.copy()
#
#     zeros = size - cv2.countNonZero(img)
#     if zeros == size:
#         done = True
#cv2.imshow('new', skel)
global m
m = []
size = []
# erode
#for k in range(200, 1000, 200):

for i in range(1, 10):
    kernel1 = np.ones((i, 3), np.uint8)
    img_erode = cv2.erode(thresh, kernel1, iterations=1, anchor=(0, 0))
    # ?cv2.imshow("new1", img_erode)
    # dilation
    # kernel2 = np.ones((1, 80), np.uint8)
    # img_dilation = cv2.dilate(img_erode, kernel2, iterations=1)

    indicator_matrix = img_erode[0:800, 0:600]
    #print(indicator_matrix)
    front, rev = test()

    all_points_in_iter.append(front)
    all_points_in_iter_rev.append(rev)



length_array = []
for i in range(0, len(all_points_in_iter), 1):
    length_array.append(len(all_points_in_iter[i]))


index, value = max(enumerate(length_array), key=operator.itemgetter(1))
set = all_points_in_iter[index]
set_rev = all_points_in_iter_rev[index]

set[0] = set_rev[0]
set_rev.remove(set_rev[0])

out_dict = {}
max_val = 0
if len(set) > len(set_rev):
    max_val = len(set)
else:
    max_val = len(set_rev)

count = 0
# print(set_rev)
# for i in range(0, len(set)-1):
#     if set[i] == set[i+1]:
#         set.remove(set[i])
# print(set_rev)
situation = False
for i in range(0, len(set)-1):
    try:
        value = set[i]
        next_val = set[i+1]
        for j in range(0, len(set_rev)):
            if value < set_rev[j] <next_val:
                situation = True

        if not situation:
            set.remove(set[i+1])
        else:
            situation = False

    except:
        pass


situation = False
for i in range(0, len(set_rev)-1):
    try:
        value = set_rev[i]
        next_val = set_rev[i+1]
        for j in range(0, len(set)):
            if value < set[j] < next_val:
                situation = True

        if not situation:
            set_rev.remove(set_rev[i])
        else:
            situation = False

    except:
        pass


situation = False

i = 0
while not situation:

    try:
        if set[i+1] - set_rev[i] < 5:

            set.remove(set[i+1])
            set_rev.remove(set_rev[i])
    except:
        situation = True
    i = i + 1


temp = 0
plot = []
del_list = []
#print(set[7], set[7])
for i in range(0, len(set)-1):
    plot.append(set[i])
    for j in range(0, len(set_rev)):

        if set[i] < set_rev[j] < set[i + 1]:
            temp = set_rev[j]

    if temp == 1:
        del_list.append(i)
    plot.append(temp)
    temp = 1
#
# #plot.append(set[len(set)-1])
#
# for i in range(0, len(set_rev)-1):
#     #plot.append(set[i])
#     for j in range(1, len(set_rev)):
#
#         if set_rev[i] < set[j] < set_rev[i + 1]:
#             temp = set[j]
#
#     if temp == 1:
#         del_list.append(i)
#     plot.append(temp)
#     temp = 1
#
plot.append(set[0])
plot.append(set_rev[len(set_rev)-1])


# for i in range(0, len(plot)-1):
#
#     value = find_mean(plot)
#
#     try:
#
#         if set[i + 1] - set[i] < value:
#             set.remove(set[i + 1])
#             #i = i - 1
#
#
#
#     except IndexError:
#         pass


# for i in range(0, len(plot), 1):
#     if i % 2 == 0:
#         cv2.line(image, (0, plot[i]), (800, plot[i]), (0, 0, 255), 1)
#     else:
#         cv2.line(image, (0, plot[i]), (800, plot[i]), (0, 255, 0), 1)

# for i in range(0, len(set), 1):
#     cv2.line(image, (0, set[i]), (800, set[i]), (0, 0, 255), 1)

# for i in range(0, len(set_rev), 1):
#     cv2.line(image, (0, set_rev[i]), (800, set_rev[i]), (255, 0, 0), 1)

cv2.imshow('final', image)
# cv2.imshow('thresh', thresh)
kernel_dil = np.ones((9, 8), np.uint8)
phase_two = cv2.dilate(thresh, kernel_dil, iterations=1, anchor=(0, 0))
counter = 0
for i in range(len(set) - 1):
    crop = phase_two[set[i]:set[i+1]][:800]
    # cv2.imshow('dil', crop)
    _, contours, hierarchy = cv2.findContours(crop, 1, 2)
    # print(len(contours))

    for cnt in contours:
        try:
            x, y, w, h = cv2.boundingRect(cnt)
            # print(x, y, w, h)
            y = y + set[counter]
            if w * h > 100:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        except:
            pass
    counter = counter + 1
cv2.imshow('New', image)
cv2.waitKey(0)

cv2.destroyAllWindows()



