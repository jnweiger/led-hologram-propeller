#! /usr/bin/python3
#
# encode_polar_bin.py -- fun with polar coordinates.

from PIL import Image
import sys, math, random

debug = False    # use small test values
verbose = False  # print everthing...

diam = 360            # input png image width
c_x = (diam-1.)/2
c_y = (diam-1.)/2
n_rays = 2700         # 113400 / 42
padsize = 1288          # number of \0 bytes between frames.
leds = 224


def quad_avg(pix_acc, x, y):
  """
     pix_acc is a https://pillow.readthedocs.io/en/latest/reference/PixelAccess.html
     x,y must be in range. E.g. Image width=360, x in [0..359],
     A small epsilon is allowed beyond the last element, as x and y are expected as
     floating point coordinates. quad_avg() returns a weighted average pixel color from
     the four neighboring pixels.
     Each channel is averaged indepently. Good for RGB, but may not work as well for HLS)
     Any number of channels.
     A tuple of rounded integer values is returned.
  """
  x0 = int(x)
  xd = x - x0
  y0 = int(y)
  yd = y - y0
  r = []
  d_eps = 0.0001
  # expect 3 colors, but any is fine.
  for col in range(len(pix_acc[0,0])):
    if xd <= d_eps:
      y0_avg = pix_acc[x0,y0][col]
      if yd > d_eps:
        y1_avg = pix_acc[x0,y0+1][col]
    else:
      y0_avg = pix_acc[x0,y0][col]   * (1-xd) + pix_acc[x0+1,y0][col]   * xd
      if yd > d_eps:
        y1_avg = pix_acc[x0,y0+1][col] * (1-xd) + pix_acc[x0+1,y0+1][col] * xd
    if yd <= d_eps:
      r.append(int(y0_avg + 0.5))
    else:
      r.append(int(y0_avg * (1-yd) + y1_avg * yd + 0.5))
  return tuple(r)


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


def rgb_byte_column(x):
  # 0 1 2 3 4 5 6 7 24 25 26 27 28 29 30 31 48 48 50 51
  return 8*3*(x//8)+(x%8)


def encode_polar_bin(imgfile):
  im = Image.open(imgfile).convert('RGB')       # make sure it is RGB
  pix = im.load()

  # prepare a frame polar distortion
  po = []
  for i in range(leds//2*3):
    po.append([])

  for n in range(n_rays):
    phi = math.radians(360.*n/n_rays)
    sca = float(diam-1)/float(leds-1)
    if verbose:
      print("n=%d\t" % n, end='')
    for led in range(leds//2):
      (x,y) = polar2cart(c_x, c_y, (0.5+led) * sca, phi)
      if verbose:
        print("(%.2f, %.2f) " % (x,y), end="")
      rgb = quad_avg(pix, x, y)
      ### bit interleaved? Nah, does not look right...
      #po[3*led+0].append(rgb[0])
      #po[3*led+1].append(rgb[1])
      #po[3*led+2].append(rgb[2])
      ### byte interleaved
      cc = rgb_byte_column(led)
      po[cc+0 ].append(rgb[0])
      po[cc+8 ].append(rgb[1])
      po[cc+16].append(rgb[2])

    if verbose:
      print("")

  ## prepare a frame for the binary format
  out = []
  for n in range(n_rays):
    out.append([0] * (3*leds//16))

  for column in range(len(po)):
    byte   =       (len(po)-1-column) // 8
    bitval = 1 << ((len(po)-1-column) % 8)
    err = 0
    for n in range(n_rays):
      # TODO: add error diffusion here
      val = po[column][n]
      if val > 87:
        out[n][byte] |= bitval;
  return out


o = open("rgb_enc_01.bin", "wb")
header = [ 0x00, 0x00, 0x00, 0x3c, 0x18 ]               # seen with Gif-Anims
# header = [ 0x00, 0x00, 0x00, 0x01, 0x18 ]             # seen with mp4
padding = bytes([0] * padsize)

for i in range(5, 0x1000):
  header.append(random.randint(0,255))
o.write(bytes(header))


for img in sys.argv[1:]:
  print("encoding %s ..." % img)
  data = encode_polar_bin(img)

  for row in data:
    o.write(bytes(row))
  o.write(padding)

o.close()

