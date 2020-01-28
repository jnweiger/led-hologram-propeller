#! /usr/bin/python3
#
# quad_avg.py -- lookup four neighbouring values and interpolate them according to distance.

pict = [ [ 1,2,34,5,6,7,8,9], [2,3,45,67,8,8,9,8], [ 4,5,6,7,8,9,10,11], [1,2,3,4,5,6,7,8] ]

def quad_avg(data, x, y):
  x0 = int(x)
  xd = x - x0
  y0 = int(y)
  yd = y - y0
  y0_avg = data[y0][x0]   * (1-xd) + data[y0][x0+1]   * xd
  y1_avg = data[y0+1][x0] * (1-xd) + data[y0+1][x0+1] * xd
  return y0_avg * (1-yd) + y1_avg * yd



