import Tkinter as tk
from PIL import Image, ImageTk
import sys

filename = sys.argv[1]
file = filename.split('/')[-1]
window = tk.Tk(className=file.split('.')[0])
boundary = []

image = Image.open(filename)
im_width, im_height = image.size
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
    if len(boundary) == 2:
        window.quit()


canvas.bind("<Button-1>", callback)
tk.mainloop()
cropped_img = image.crop(boundary[0] + boundary[1])
cropped_name = sys.argv[2] + file
print 'saving as', cropped_name
cropped_img.save(cropped_name)
