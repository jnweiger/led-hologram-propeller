#! /usr/bin/python3

from PIL import Image, ImageDraw

image = Image.new("RGBA", (448, 448), "#000")
draw = ImageDraw.Draw(image, image.mode)
for i in reversed(range(256)):
  draw.pieslice((0, 0 , 448, 448), 0, 360*i/255, fill=(i,0,i))

del draw
image.save("arc_magenta_shades.png", "PNG")

