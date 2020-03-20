#! /usr/bin/python3
#
# 

def ordered_dith(x, y, val):
  """ val is expected in 0...255
      x is used modulo 2
      y is used modulo 12

      The dither pattern has 13 different values. We duplicate the first and the last value to 
      stretch the typical video range of [16..240] back into [0..255]
  """
  dith = (
    ( 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0 ),
    ( 1, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0 ),
    ( 1, 0, 0, 0, 0, 0,  1, 0, 0, 0, 0, 0 ),
    ( 1, 1, 0, 0, 0, 0,  1, 0, 0, 0, 0, 0 ),
    ( 1, 1, 0, 0, 0, 0,  1, 1, 0, 0, 0, 0 ),
    ( 1, 1, 1, 0, 0, 0,  1, 1, 0, 0, 0, 0 ),
    ( 1, 1, 1, 0, 0, 0,  1, 1, 1, 0, 0, 0 ),
    ( 1, 1, 1, 1, 0, 0,  1, 1, 1, 0, 0, 0 ),
    ( 1, 1, 1, 1, 0, 0,  1, 1, 1, 1, 0, 0 ),
    ( 1, 1, 1, 1, 1, 0,  1, 1, 1, 1, 0, 0 ),
    ( 1, 1, 1, 1, 1, 0,  1, 1, 1, 1, 1, 0 ),
    ( 1, 1, 1, 1, 1, 1,  1, 1, 1, 1, 1, 0 ),
    ( 1, 1, 1, 1, 1, 1,  1, 1, 1, 1, 1, 1 ),
    ( 1, 1, 1, 1, 1, 1,  1, 1, 1, 1, 1, 1 )
  )
  val = max(0, min(255, int(val)))      # clamp and
  v14 = int(val / 17.01)                # squeeze into [0..14]
  d = dith[v14]
  y += 6 * (int(x) % 2)
  return d[int(y) % 12]

