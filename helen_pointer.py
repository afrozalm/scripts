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
    elif pts in xrange(1, 42):
        print 'click for face boundary(1, 42)', pts
    elif pts in xrange(42, 59):
        print 'click for nose boundary(42, 59)', pts
    elif pts in xrange(59, 73):
        print 'click for lips outer upper(59, 73)', pts
    elif pts in xrange(73, 86):
        print 'click for lips outer lower(73, 86)', pts
    elif pts in xrange(86, 101):
        print 'click for lips inner upper(86, 101)', pts
    elif pts in xrange(101, 115):
        print 'click for lips inner lower(101, 115)', pts
    elif pts in xrange(115, 126):
        print 'click for right eye upper(115, 126)', pts
    elif pts in xrange(126, 135):
        print 'click for right eye lower(126, 135)', pts
    elif pts in xrange(135, 146):
        print 'click for left eye upper(135, 146)', pts
    elif pts in xrange(146, 155):
        print 'click for left eye lower(146, 155)', pts
    elif pts in xrange(155, 166):
        print 'click for right eyebrow upper(155, 166)', pts
    elif pts in xrange(166, 175):
        print 'click for right eyebrow lower(166, 175)', pts
    elif pts in xrange(175, 186):
        print 'click for left eyebrow upper(175, 186)', pts
    elif pts in xrange(186, 195):
        print 'click for left eyebrow lower(186, 195)', pts


canvas.bind("<Button-1>", callback)
tk.mainloop()
with open('../annotation/' + file + '.txt', 'wb') as f:
    f.write(os.path.abspath(filename))
    for pt in boundary:
        f.write('\n')
        f.write(str(pt[0]) + ' , ' + str(pt[1]))
