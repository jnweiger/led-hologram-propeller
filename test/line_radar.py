#! /usr/bin/python3
#
# dotanim.py -- create an gif animation where a vertival line moves right.
# https://pillow.readthedocs.io/en/latest/releasenotes/3.4.0.html#append-images-to-gif
# https://github.com/python-pillow/Pillow/blob/master/src/PIL/GifImagePlugin.py

import os
from PIL import Image, ImageDraw, ImageColor

w = 640
h = 480

col=ImageColor.getrgb("#3fff7f")

frames = []

for frame in range(h//16):
  im = Image.new("RGB", (w, h))
  draw = ImageDraw.Draw(im)
  draw.line([(w//2,h//2), (w, h//2 + 8*frame)], fill=col, width=8)
  frames.append(im)

for frame in range(w//8):
  im = Image.new("RGB", (w, h))
  draw = ImageDraw.Draw(im)
  draw.line([(w//2,h//2), (w-8*frame, h)], fill=col, width=8)
  frames.append(im)

for frame in range(h//8):
  im = Image.new("RGB", (w, h))
  draw = ImageDraw.Draw(im)
  draw.line([(w//2,h//2), (0, h-8*frame)], fill=col, width=8)
  frames.append(im)

for frame in range(w//8):
  im = Image.new("RGB", (w, h))
  draw = ImageDraw.Draw(im)
  draw.line([(w//2,h//2), (8*frame, 0)], fill=col, width=8)
  frames.append(im)

for frame in range(h//16):
  im = Image.new("RGB", (w, h))
  draw = ImageDraw.Draw(im)
  draw.line([(w//2,h//2), (w, 8*frame)], fill=col, width=8)
  frames.append(im)

frames[0].save('line_radar.gif', format='GIF', append_images=frames[1:], save_all=True, duration=int(1000./15), loop=0)

