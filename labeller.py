from PIL import Image
from itertools import product
import numpy as np
import os
from matplotlib import pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def lies_in(bound, x, y):
    polygon = map(lambda x: map(int, x.split(',')), bound)
    polygon = Polygon(polygon)
    point = Point(x, y)

    return polygon.contains(point)


def get_label(x, y, lines):
    # face_bound = lines[1:41]
    nose_bound = lines[42:59]   # 1

    lips_out_u = lines[59:73]
    lips_in_u = lines[87:101]
    lips_upper = lips_out_u + lips_in_u  # 2

    lips_in_l = lines[101:115]
    lips_out_l = lines[73:87]
    lips_lower = lips_in_l + lips_out_l  # 3

    eye_right_u = lines[115:125]
    eye_right_l = lines[125:135]
    eye_right = eye_right_u + eye_right_l  # 4

    eye_left_u = lines[135:145]
    eye_left_l = lines[145:155]
    eye_left = eye_left_u + eye_left_l  # 5

    eyebr_right_u = lines[155:165]
    eyebr_right_l = lines[165:175]
    eyebr_right = eyebr_right_u + eyebr_right_l  # 6

    eyebr_left_u = lines[175:185]
    eyebr_left_l = lines[185:195]
    eyebr_left = eyebr_left_u + eyebr_left_l  # 7

    # if lies_in(face_bound, x, y):
    #     return 1
    if lies_in(nose_bound, x, y):
        return 1
    elif lies_in(lips_upper, x, y):
        return 2
    elif lies_in(lips_lower, x, y):
        return 3
    elif lies_in(eye_right, x, y):
        return 4
    elif lies_in(eye_left, x, y):
        return 5
    elif lies_in(eyebr_right, x, y):
        return 6
    elif lies_in(eyebr_left, x, y):
        return 7
    else:
        return 0


def make_annot_tensors(lines):
    addr = lines[0]

    img = Image.open(addr)
    img.load()
    img = np.asarray(img)
    h, w, _ = img.shape
    label = np.zeros([h, w])
    # do a x, y traversal and check if point lies in any of the regions
    for x, y in product(xrange(h), xrange(w)):
        label[x][y] = get_label(y, x, lines)
    return label


DST = '../annotation/labeled-tensors/'
SRC = '../annotation'

files = []
for root, dirs, f in os.walk(SRC):
    files += f

for annotation_file in files:
    if annotation_file.split('.')[-1] != 'txt':
        continue
    outname = DST + annotation_file.split('.')[0]
    annotation_file = os.path.join(SRC, annotation_file)
    print 'processing', annotation_file
    with open(annotation_file) as f:
        lines = f.read().splitlines()

    label = make_annot_tensors(lines)
    np.save(outname, label)
    plt.imshow(label)
    plt.imsave(outname, label)
