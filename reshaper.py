import numpy as np
from collections import Iterable
import pickle
import os
from random import sample
from scipy.misc import imresize
from scipy.ndimage.interpolation import rotate
from PIL import Image
from multiprocessing.dummy import Pool
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-real', action='store_true')
parser.add_argument('-subsample', action='store_true')
parser.add_argument('-normed', action='store_true')
parser.add_argument('-width', type=int, default=64)
option = parser.parse_args()

suffix = '_' + str(option.width) + 'x' + str(option.width) + '/'
if not option.real:
    SRC = '/home/afrozalm/data/cropped'
    DST = '/home/afrozalm/data/reshaped_cropped' + suffix
else:
    SRC = '/home/afrozalm/data/cropped_real'
    DST = '/home/afrozalm/data/reshaped_cropped_real' + suffix

if option.normed:
    normed = True
    SUFFIX = '_normed.pkl'
else:
    normed = False
    SUFFIX = '.pkl'

if not os.path.exists(DST):
    os.mkdir(DST)
# they come in height x width x channels
subsample_mode = option.subsample
sample_size = 200
subsample_height = option.width
subsample_width = option.width
n_threads = 6


def normalize(v):
    '''
    this function takes as input a 3d image
    ndarray and returns the normalized ndarray
    '''
    if normed:
        v_min = v.min(axis=(0, 1), keepdims=True)
        v_max = v.max(axis=(0, 1), keepdims=True)
        return (v - v_min) / (v_max - v_min)
    return v


def remover(x): return ''.join([i for i in x if not i.isdigit()])


def get_label(name):
    if 'Peter_Dinklage' in name:
        name =  ''.join([i for i in name if not (i == 'l')])
    name = name.split('/')[-1]
    name = name.rsplit('.', 1)[0]
    return remover(name)


def convert(filename):
    '''
    takes name of an image in Selection folder
    and converts it into numpy array
    '''
    global DST
    img = Image.open(filename)
    img.load()
    img = np.asarray(img)
    mean = np.mean(img)
    angle = 10.0

    img_resized = resize(img)
    img_rot_clock = resize(rotate(img, angle=angle, cval=mean))
    img_rot_anti_clock = resize(rotate(img, angle=-angle, cval=mean))

    img_flipped = np.fliplr(img)
    img_flipped_resized = resize(img_flipped)
    img_flipped_clock = resize(rotate(img_flipped, angle=angle, cval=mean))
    img_flipped_anti_clock = resize(rotate(img_flipped, angle=-angle, cval=mean))

    destination_name = DST + filename.split('/')[-1]
    Image.fromarray(img_flipped_anti_clock).save(destination_name)
    label = get_label(filename)
    return [(normalize(img_resized), label),
            (normalize(img_rot_clock), label),
            (normalize(img_rot_anti_clock), label),
            (normalize(img_flipped_resized), label),
            (normalize(img_flipped_clock), label),
            (normalize(img_flipped_anti_clock), label)]


def resize(t):  # t is a np array
    if len(t.shape) == 2:
        ht, wd = t.shape
        t = t.reshape((ht, wd, 1)) + np.ones(3)
    elif t.shape[2] == 4:
        ht, wd, _ = t.shape
        t = t[:, :, :3]
    else:
        ht, wd, _ = t.shape

    major = 0 if ht > wd else 1
    mean = np.mean(t)
    if major == 0:
        new_t = np.ndarray((ht, ht, 3), dtype=t.dtype)
        new_t.fill(mean)
        offset = (ht - wd) / 2
        new_t[:, offset:offset + wd, :] = t
    else:
        new_t = np.ndarray((wd, wd, 3), dtype=t.dtype)
        new_t.fill(mean)
        offset = (wd - ht) / 2
        new_t[offset:offset + ht, :, :] = t
    return imresize(new_t, (subsample_height, subsample_width, 3))


def flatten(lis):
    for item in lis:
        if isinstance(item, list):
            for x in flatten(item):
                yield x
        else:
            yield item

img_paths = []
for root, dirs, files in os.walk(SRC):
    for file in files:
        img_paths.append(root + os.sep + file)

if subsample_mode:
    img_paths = img_paths[:sample_size]

pool = Pool(n_threads)
array_list = pool.map(convert, img_paths)
pool.close()
pool.join()
# array_list = map(convert, img_paths)

img_tensors = list(flatten(array_list))


def save_pkl(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        print ('Saved %s..' % path)


if not subsample_mode:
    save_pkl(img_tensors, DST + 'fullset' + SUFFIX)

subsample_tensors = sample(array_list, 200)
sample_train = subsample_tensors[:100]
sample_test = subsample_tensors[100:160]
sample_val = subsample_tensors[160:200]

save_pkl(sample_train, DST + 'sample_train' + SUFFIX)
save_pkl(sample_test, DST + 'sample_test' + SUFFIX)
save_pkl(sample_val, DST + 'sample_val' + SUFFIX)

print img_tensors[0][1], len(img_tensors)
