#! /usr/bin/python3
#
# polar.py -- fun with polar coordinates.

import math

diam = 36
c_x = (diam-1.)/2
c_y = (diam-1.)/2
n_rays = 240
leds = 22

def polar2cart(cx, cy, r, phi):
  """
      clock position    phi 
        3h              math.radians(0) = 0
        1h30            math.radians(45)
        12h             math.radians(90)
        9h              math.radians(180)
        6h              math.radians(270)
        4h30            math.radians(315)
   """
  x = cx + r * math.cos(phi)
  y = cy + r * math.sin(phi)
  return (x, y)
 

for n in range(n_rays):
  phi = math.radians(360.*n/n_rays)
  sca = float(diam-1)/float(leds-1)
  print("n=%d\t" % n, end='')
  for led in range(leds//2):
    print("(%.2f, %.2f) " % polar2cart(c_x, c_y, (0.5+led) * sca, phi), end="")
  print("")
