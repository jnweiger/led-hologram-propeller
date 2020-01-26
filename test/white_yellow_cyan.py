#! /usr/bin/python3
#
# white_yellow_cyan.py -- alternate three solid frame colors
# https://pillow.readthedocs.io/en/latest/releasenotes/3.4.0.html#append-images-to-gif
# https://github.com/python-pillow/Pillow/blob/master/src/PIL/GifImagePlugin.py

import os
from PIL import Image

w = 224*2
h = 224*2

def putdot(data, x, y, color=(255,255,255), size=(2,2)):
  """ Paint a rectangular group of pixels.
      Out of bounds operations are harmlessly ignored
  """
  for j in range(int(size[1])):
    for i in range(int(size[0])):
      try:
        data[int(x+i), int(y+j)] = color
      except:
        pass
 

frames = []

cols=[(255,255,255), (255,255,0), (0,255,255), (255,0,255)]

for i in range(1):
  for col in cols:
    im = Image.new("RGB", (w, h))
    pix = im.load()
    putdot(pix, 0, 0, color=col, size=(w,h))
    # BUG-Alert: The save() method computes the palette for all images from the first image. Need to show all colors there.
    for p in range(len(cols)):
      putdot(pix, w*3/4+2*p, h/2+2, color=cols[p])
    frames.append(im)

frames[0].save('gif/white_yellow_cyan_30fps.gif', format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./30), loop=1)
frames[0].save('gif/white_yellow_cyan_25fps.gif', format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./25), loop=1)
frames[0].save('gif/white_yellow_cyan_15fps.gif', format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./15), loop=1)
frames[0].save('gif/white_yellow_cyan_10fps.gif', format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./10), loop=1)
frames[0].save('gif/white_yellow_cyan_5fps.gif',  format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./5),  loop=1)
frames[0].save('gif/white_yellow_cyan_2fps.gif',  format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./2),  loop=1)

