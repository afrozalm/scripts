import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-real', action='store_true')
option = parser.parse_args()

if not option.real:
    SRC = '../scraped_data2/'
    DST = ' ../cropped/'
else:
    SRC = '../scraped_data_real2/'
    DST = ' ../cropped_real/'

print DST
for root, dirs, files in os.walk(SRC):
    for file in files:
        cmd = 'python crop_helper.py ' + root + os.sep + file + DST
        print 'executing', cmd
        os.system(cmd)

print 'finished'
