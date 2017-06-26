import subprocess
import sys
import tty
import termios
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-real', action='store_true')
option = parser.parse_args()

if not option.real:
    DST = '../scraped_data/'
else:
    DST = '../scraped_data_real/'


class _GetchUnix:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


reader = _GetchUnix()
for root, dirs, files in os.walk(DST):
    if len([name for name in os.listdir(root)]) == 40:
        for file in files:
            filename = root + os.sep + file
            p = subprocess.Popen(["display", filename])
            k = reader()
            if k == 'k':
                # keeping this one
                pass
            else:
                try:
                    os.remove(filename)
                    print 'deleting ', filename
                except:
                    pass
            p.kill()
