import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-real', action='store_true')
option = parser.parse_args()

if not option.real:
    SRC = '../cropped'
else:
    SRC = '../cropped_real'

for root, dirs, files in os.walk(SRC):
    for file in files:
        cmd = 'python helen_pointer.py  ' + root + os.sep + file
        print 'executing', cmd
        os.system(cmd)

print 'finished'
