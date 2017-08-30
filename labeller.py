from PIL import Image
from itertools import product
import numpy as np
import os


def same_side(pt, prev_pt, mid_pt, next_pt):

    return True


def lies_in(bound, x, y):
    prev_pt = map(int, bound[0].split(','))
    mid_pt = map(int, bound[1].split(','))
    for next_pt in bound[2:]:
        next_pt = map(int, next_pt.split(','))
        if not same_side([x, y], prev_pt, mid_pt, next_pt):
            return False
        prev_pt = mid_pt
        mid_pt = next_pt

    return True


def get_label(x, y, lines):
    face_bound = lines[1:41]    # 1
    nose_bound = lines[41:58]   # 2
    lips_out_u = lines[58:72]   # 3
    lips_out_l = lines[72:86]   # 4
    lips_in_u = lines[86:100]   # 5
    lips_in_l = lines[100:114]  # 6
    eye_right_u = lines[114:124]  # 7
    eye_right_l = lines[124:134]  # 8
    eye_left_u = lines[134:144]   # 9
    eye_left_l = lines[144:154]   # 10
    eyebr_right_u = lines[154:164]  # 11
    eyebr_right_l = lines[164:174]  # 12
    eyebr_left_u = lines[174:184]   # 13
    eyebr_left_l = lines[184:194]   # 14

    if lies_in(face_bound, x, y):
        return 1
    elif lies_in(nose_bound, x, y):
        return 2
    elif lies_in(lips_out_u, x, y):
        return 3
    elif lies_in(lips_out_l, x, y):
        return 4
    elif lies_in(lips_in_u, x, y):
        return 5
    elif lies_in(lips_in_l, x, y):
        return 6
    elif lies_in(eye_right_u, x, y):
        return 7
    elif lies_in(eye_right_l, x, y):
        return 8
    elif lies_in(eye_left_u, x, y):
        return 9
    elif lies_in(eye_left_l, x, y):
        return 10
    elif lies_in(eyebr_right_u, x, y):
        return 11
    elif lies_in(eyebr_right_l, x, y):
        return 12
    elif lies_in(eyebr_left_u, x, y):
        return 13
    elif lies_in(eyebr_left_l, x, y):
        return 14
    else:
        return 0


def make_annot_tensors(lines):
    addr = lines[0]

    img = Image.open(addr)
    img.load()
    img = np.asarray(img)
    h, w, _ = img.shape
    # mask = np.zeros([h, w])
    label = np.zeros([h, w])
    # do a x, y traversal and check if point lies in any of the regions
    for x, y in product(xrange(h), xrange(w)):
        label[x][y] = get_label(x, y, lines)


DST = '../annotation/labeled-tensors'
SRC = '../annotation'

files = []
for root, dirs, f in os.walk(SRC):
    files += f

for annotation_file in files:
    with open(annotation_file) as f:
        lines = f.read().splitlines()

    make_annot_tensors(lines)
