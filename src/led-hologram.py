#! /usr/bin/python3
# -*- encoding: utf-8 -*-
#
# (C) 2020 juergen@fabmail.org
#
# This is an upload tool for Holographich 3D Advertising machines with 224 LEDs.
# E.g. from
# - https://hologramdisplay3d.com/the-hologram-display-led-fan/the-hologram-display-led-fan-377.html
# - https://www.aliexpress.com/item/33026727586.html
#
# The device comes with a WiFi interface. This allows upload and change of the animation without stopping the propeller.
# The propeller has a 16GB SDcard, where the animations are stored in a special 'bin' format.
#
# v0.1, 2020-01-21, jw  initial draught. Simple pause, play, and status commands done.
# v0.2, 2020-01-22, jw  delete command added.
#

from __future__ import print_function
import sys, os, re, socket, argparse

__version = "0.2"

default_ip_addr = '192.168.4.1'
default_tcp_port = '5233'
default_tcp_magic_port = '5499'

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='Control a 224 LED holographic propeller display.\nVersion %s from https://github.com/jnweiger/led-hologram-propeller\n -- see there for more examples and for updates.' % __version, epilog="""
Commands:

  pause
    Stop the animation at the current frame. A constant image will be shown until a
    'play' command is sent.

  play
    Resume playing. Unpause.

  status
    Show list of uploaded files, marking the one that is currently playing.

  delete NN
    Remove a file from the list.
    NN should be an index number from the first column of the status output.

""")

parser.add_argument('-a', '--address', default=default_ip_addr, help="IP-Addess of the device. Default: %s" % default_ip_addr)
parser.add_argument('-p', '--port', default=default_tcp_port, help="TCP port to connect with the device. Default: %s" % default_tcp_port)
parser.add_argument('-M', '--magicport', default=default_tcp_magic_port, help="TCP port that returns the magic string. Default: %s" % default_tcp_magic_port)
parser.add_argument('cmd', metavar='COMMAND', nargs='+', help="Command word.")
parser.add_argument('--command-help', action='version', help=argparse.SUPPRESS, version="--")
args = parser.parse_args()
# print(args)

def try_recv(s, timeout=0.2, verbose=False):
  s.settimeout(timeout)       # seconds
  buf = ''
  try:
    buf = s.recv(1024)
    if buf and verbose:
      print("received %s" % buf)
  except socket.timeout:
    pass
  return buf


def fmt_status(msg):
  """
  pause received b'c0eeb7c9baa3020000000012cc38lnt200100_green_earth.bin200201_green_earth.bin220302_spinning_coin.bin220403_spinning_coin.bin230504_bouncing_fraph.bin230605_spinning_heart.bin02HE10bfb5d2a2'
  play  received b'c0eeb7c9baa3020000000012cc38lnt200100_green_earth.bin200201_green_earth.bin220302_spinning_coin.bin220403_spinning_coin.bin230504_bouncing_fraph.bin230605_spinning_heart.bin02HE11bfb5d2a2'
  play  received b'c0eeb7c9baa3020000000012cc38lnt200100_green_earth.bin200201_green_earth.bin220302_spinning_coin.bin220403_spinning_coin.bin230504_bouncing_fraph.bin230605_spinning_heart.bin04HE11bfb5d2a2'
  play  received b'c0eeb7c9baa3020000000012cc38lnt200100_green_earth.bin200201_green_earth.bin220302_spinning_coin.bin220403_spinning_coin.bin230504_bouncing_fraph.bin230605_spinning_heart.bin05HE11bfb5d2a2'
  play  received b'c0eeb7c9baa3020000000012cc38lnt200100_green_earth.bin200201_green_earth.bin220302_spinning_coin.bin220403_spinning_coin.bin230504_bouncing_fraph.bin230605_spinning_heart.bin06HE11bfb5d2a2'
  """
  trailer = msg[-14:]   # 02HE10bfb5d2a2
  if trailer[2:4] != b'HE':
    print("ERROR: trailer mismatch. did it change size? Trailer: %s" % trailer)
    sys.exit(1)

  # never fetch a single element from a bytes array! b'1' becomes 49 then. Nice, but not useful here.
  if trailer[5:6] == b'1':
    marker = '>>'   # playing
  elif trailer[5:6] == b'0':
    marker = '||'   # paused
  else:
    marker = '?' + trailer[5:6].decode('UTF-8')   # unknown flag
  prefix = msg[0:31]
  l = msg[31:]
  li = {}
  while True:
    try:
      n = int(l[0:2])
    except:
      break
    if l[2:4] == b'HE':         # trailer found
      break
    li[l[2:4].decode('UTF-8')] = l[4:2+n].decode('UTF-8')
    l = l[2+n:]
  for i in sorted(li.keys()):
    if trailer[:2].decode('UTF-8') == i:
      print("%2s %2s| %s" % (marker, i, li[i]))
    else:
      print("   %2s| %s" % (i, li[i]))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3.0)       # seconds
s.connect((args.address, int(args.port)))
try_recv(s, 0.1, True)

if args.cmd[0] == 'pause':
  n = s.send(b"c0eeb7c9baa3020000000014cc" + b"34" + b"lfhbfb5d2a2")
  print("%d bytes sent." % n)

elif args.cmd[0] == 'play':
  n = s.send(b"c0eeb7c9baa3020000000014cc" + b"35" + b"lfhbfb5d2a2")
  print("%d bytes sent." % n)

elif args.cmd[0] == 'status':
  n = s.send(b"c0eeb7c9baa3020000000014cc" + b"38" + b"lfhbfb5d2a2")
  fmt_status(try_recv(s, 2.0, False))

elif args.cmd[0] == 'del' or args.cmd[0] == 'delete':
  if len(args.cmd) < 2:
    print("ERROR: delete needs an INDEX parameter.")
    sys.exit(1)
  idx = int(args.cmd[1])
  if idx <= 0 or idx > 99:
    print("ERROR: delete INDEX must be > 1 and < 100. (%d seen)" % idx)
    sys.exit(1)
  n = s.send(b"c0eeb7c9baa3020000000014cc" + b"39" + b"lfj" + bytes("%02d" % idx, "UTF-8") + b"bfb5d2a2")
  print("%d bytes sent." % n)

else:
  print("\nUnknown command '%s' -- try %s --help" % (args.cmd[0], sys.argv[0]))

try_recv(s, 0.5, True)


# magic seen from port 5499:
# d3e0c9ba02012dd80AfJ0000bfb5d2a2
# hmm, that seems to be unused.
