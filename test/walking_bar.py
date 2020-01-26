#! /usr/bin/python3
#
# dotanim.py -- create an gif animation where a vertival line moves right.
# https://pillow.readthedocs.io/en/latest/releasenotes/3.4.0.html#append-images-to-gif

import os
from PIL import Image

w = 640
h = 480

def putdot(data, x, y, color=(255,255,255), size=(2,2)):
  """ Paint a rectangular group of pixels.
      Out of bounds operations are harmlessly ignored
  """
  for j in range(size[0]):
    for i in range(size[0]):
      try:
        data[int(x+i), int(y+j)] = color
      except:
        pass
 

try:
  os.mkdir("bar")
except:
  pass

frames = []

for frame in range(200):  
  im = Image.new("RGB", (w, h))
  pix = im.load()
  for y in range(h):
    putdot(pix,w/2-1+frame, y)
  im.save("bar/frame_%03d.png" % frame)
  frames.append(im)

frames[0].save('walking_bar.gif', format='GIF', append_images=frames[1:], save_all=True, duration=1, loop=0)

