#! /usr/bin/python3
#
# dotanim.py -- create an gif animation where a vertival line moves right.
# https://pillow.readthedocs.io/en/latest/releasenotes/3.4.0.html#append-images-to-gif
# https://github.com/python-pillow/Pillow/blob/master/src/PIL/GifImagePlugin.py

import os
from PIL import Image, ImageDraw, ImageColor

w = 224*2
h = 224*2

col=ImageColor.getrgb("#3fff7f")

frames = []

for pad in range(2,20):
  im = Image.new("RGB", (w, h))
  draw = ImageDraw.Draw(im)
  draw.ellipse([(0+4*pad-10,0+4*pad-10), (w-4*pad+10,h-4*pad+10)], fill=col)
  draw.ellipse([(0+4*pad+10,0+4*pad+10), (w-4*pad-10,h-4*pad-10)], fill=(0,0,0))
  draw.ellipse([(0+4*pad+90,0+4*pad+90), (w-4*pad-90,h-4*pad-90)], fill=(255,0,0))
  frames.append(im)

for pad in range(20,2,-1):
  im = Image.new("RGB", (w, h))
  draw = ImageDraw.Draw(im)
  draw.ellipse([(0+4*pad-10,0+4*pad-10), (w-4*pad+10,h-4*pad+10)], fill=col)
  draw.ellipse([(0+4*pad+10,0+4*pad+10), (w-4*pad-10,h-4*pad-10)], fill=(0,0,0))
  frames.append(im)

frames[0].save('gif/circles.gif', format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./15), loop=0)

