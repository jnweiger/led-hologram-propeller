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
# v0.3, 2020-01-23, jw  started upload command.
#

from __future__ import print_function
import sys, os, math, socket, argparse


__version = "0.3"

default_ip_addr = '192.168.4.1'
default_tcp_port = '5233'
default_tcp_upload_port = '5499'

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

  upload FILE.bin
    Load a file into the device. The '.bin' suffix is mandatory.

""")

parser.add_argument('-a', '--address', default=default_ip_addr, help="IP-Addess of the device. Default: %s" % default_ip_addr)
parser.add_argument('-p', '--port', default=default_tcp_port, help="TCP port to connect with the device. Default: %s" % default_tcp_port)
parser.add_argument('-M', '--upload-port', default=default_tcp_upload_port, help="TCP port for file upload. Default: %s" % default_tcp_upload_port)
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


def upload_bin_file(address, port, file):
  print("upload_bin_file('%s', %d, '%s')" % (address, port, file))
  #u = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #u.settimeout(0.1)       # seconds
  #u.connect((address, int(port)))
  #try_recv(u, 0.1, False)
  #u.close()
  fname = file.split('/')[-1]
  fname_b = bytes(fname, 'UTF-8')
  if fname[-4:] != '.bin':
    print("upload_file: ERROR: need a filename with '.bin' suffix. Got: '%s'" % fname)
    sys.exit(1)
  if len(fname_b) > 99:
    print("upload_file: ERROR: filename '%s' is %d bytes long. Maximum: 99" %(fname, len(fname_b)))
    sys.exit(1)

  PACKET_SIZE=1460
  PACKET_HEADER="d3e0c9ba02014dd81GnH"
  PACKET_TRAILER="bfb5d2a2"

  fsize = os.stat(file).st_size
  chunksize = PACKET_SIZE - len(PACKET_HEADER) - len(PACKET_TRAILER)
  npackets = math.ceil(float(fsize)/chunksize)
  padsize = (npackets * chunksize) - fsize
  print("fsize=%d, chunksize=%d, npackets=%d, padsize=%d" % (fsize, chunksize, npackets, padsize))

  # d3e0c9ba02014dd80AgQ.F.(02_spinning_coin.binbfb5d2a2
  # b'd3e0c9ba02014dd80AgQ\x00F\x13(02_spinning_coin.binbfb5d2a2'
  msg = (b"d3e0c9ba0%d14dd80AgQ" % len(fname_b)) + bytes([0x00, 0x46, 0x13, 0x28]) + fname_b + b"bfb5d2a2"
  print(msg)
  #n = s.send(msg)

  unfinished.



#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.settimeout(3.0)       # seconds
#s.connect((args.address, int(args.port)))
#try_recv(s, 0.1, True)

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

elif args.cmd[0] == 'upload':
  if len(args.cmd) < 2:
    print("ERROR: upload needs an binfile parameter.")
    sys.exit(1)
  upload_bin_file(args.address, int(args.upload_port), args.cmd[1])

else:
  print("\nUnknown command '%s' -- try %s --help" % (args.cmd[0], sys.argv[0]))

#try_recv(s, 0.5, True)


# magic seen from port 5499:
# d3e0c9ba02012dd80AfJ0000bfb5d2a2
# hmm, that seems to be unused.
