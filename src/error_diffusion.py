#! /usr/bin/python3
#
# error_diffusion.py -- one-dimensional error diffusion for rotational displays
# 
# Reference: https://en.wikipedia.org/wiki/Error_diffusion#One-dimensional_error_diffusion
# 
# The simplest form of the algorithm scans the image one row at a time and one pixel at a time.
# The current pixel is compared to a half-gray value. If it is above the value a white pixel
# is generated in the resulting image. If the pixel is below the half way brightness, a black
# pixel is generated. The generated pixel is either full bright, or full black, so there is
# an error in the image. The error is then added to the next pixel in the image and the process repeats.
#


max = 255
med = 127
line = []
for i in range(max+1): line.append(i)
for i in range(max+1): line.append(255-i)

print(line)

out = []
err = 0
for i in range(len(line)):
  v = err + line[i]
  if v > med:
    out.append(1)
    err = v-255
  else:
    out.append(0)
    err = v

print(out)
