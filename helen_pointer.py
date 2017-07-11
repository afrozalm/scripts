import Tkinter as tk
from PIL import Image, ImageTk
import sys
import os

filename = sys.argv[1]
file = filename.split('/')[-1]
file = file.split('.')[0]
window = tk.Tk(className=file)
boundary = []

image = Image.open(filename)
im_width, im_height = image.size
if im_width == 64 and im_height == 64:
    print 'A 64x64 image; not annotating'
    exit(0)
ratio = min(1000.0 / im_height, 1000.0 / im_width, 1)
image = image.resize((int(im_width * ratio),
                      int(im_height * ratio)))
canvas = tk.Canvas(
    window, width=image.size[0], height=image.size[1])
canvas.pack()
image_tk = ImageTk.PhotoImage(image)
canvas.create_image(image.size[0] // 2,
                    image.size[1] // 2, image=image_tk)

print 'cropping', filename


def callback(event):
    print "clicked at: ", event.x, event.y
    boundary.append((event.x, event.y))
    pts = len(boundary)
    if pts == 194:
        window.quit()
    elif pts in xrange(1, 41):
        print 'click for face boundary(1, 41)', 41 - pts, 'points left'
    elif pts in xrange(41, 58):
        print 'click for nose boundary(41, 58)', 58 - pts, 'points left'
    elif pts in xrange(58, 72):
        print 'click for lips outer upper(58, 72)', 72 - pts, 'points left'
    elif pts in xrange(72, 86):
        print 'click for lips outer lower(72, 86)', 86 - pts, 'points left'
    elif pts in xrange(86, 100):
        print 'click for lips inner upper(86, 100)', 100 - pts, 'points left'
    elif pts in xrange(100, 114):
        print 'click for lips inner lower(100, 114)', 114 - pts, 'points left'
    elif pts in xrange(114, 124):
        print 'click for right eye upper(114, 124)', 124 - pts, 'points left'
    elif pts in xrange(124, 134):
        print 'click for right eye lower(124, 134)', 134 - pts, 'points left'
    elif pts in xrange(134, 144):
        print 'click for left eye upper(134, 144)', 144 - pts, 'points left'
    elif pts in xrange(144, 154):
        print 'click for left eye lower(144, 154)', 154 - pts, 'points left'
    elif pts in xrange(154, 164):
        print 'click for right eyebrow upper(154, 164)', 164 - pts, 'pts left'
    elif pts in xrange(164, 174):
        print 'click for right eyebrow lower(164, 174)', 174 - pts, 'pts left'
    elif pts in xrange(174, 184):
        print 'click for left eyebrow upper(174, 184)', 184 - pts, 'pts left'
    elif pts in xrange(184, 194):
        print 'click for left eyebrow lower(184, 194)', 194 - pts, 'pts left'


canvas.bind("<Button-1>", callback)
tk.mainloop()
with open('../annotation/' + file + '.txt', 'wb') as f:
    f.write(os.path.abspath(filename))
    for pt in boundary:
        f.write('\n')
        f.write(str(pt[0]) + ' , ' + str(pt[1]))
