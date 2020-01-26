#! /usr/bin/python3
#
# dotanim.py -- create an gif animation where a vertival line moves right.
# https://pillow.readthedocs.io/en/latest/releasenotes/3.4.0.html#append-images-to-gif
# https://github.com/python-pillow/Pillow/blob/master/src/PIL/GifImagePlugin.py

import os
from PIL import Image

w = 640
h = 480

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

for frame in range(20):  
  im = Image.new("RGB", (w, h))
  pix = im.load()
  if frame & 3 == 0:
    putdot(pix, 0, 0, color=(255,255,0), size=(w/2, h/2))
  elif frame & 3 == 1:
    putdot(pix, w/2, 0, color=(255,255,0), size=(w/2, h/2))
  elif frame & 3 == 2:
    putdot(pix, w/2, h/2, color=(255,255,0), size=(w/2, h/2))
  else:
    putdot(pix, 0, h/2, color=(255,255,0), size=(w/2, h/2))
  frames.append(im)

frames[0].save('flicker_quad_cw.gif', format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./15), loop=0)

