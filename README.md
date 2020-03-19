# led-hologram-propeller
Driver for a POV display device with 224 LEDs, also called Led fan, 3D-Holographic display and other fancy names in marketing

This implements the rectangular to polar coordinate transformation required for the display.
In the inner parts, the destination has higher resolution, in the outer parts, the source has higher resolution.
That makes it hard to apply a standard algorithm.

Idea: Scale the input picture down (or up) to ca. 2 times (or only 1.5 times) the diameter,
then sample the source image with a 3x3 convolution kernel using polar coordinates.
In the inner parts they hugely overlap, smearing a few source pixels along very different angular values.
In the outer parts, there may be the case, that we don't send enough rays to avoid gaps.
If needed send 2,3,4 rays for each scan line and average them.

Challenge: find a way to apply a convolution kernel to an (x,y) kernel and get the value.

check out the implementation of ImageOps.expand and im.filter()


The outermost ring is 0, counting inwards:
```
Byte Bit     Ring Color
----+------------+-------
   0 7		0 Blue
   0 6		0 Green
   0 5		0 Red
   0 4		1 Bue
   0 3		1 Green
   0 2		1 Red
   0 1		2 Blue
   0 0		2 Green

   0 7		2 Red
   0 6		3 Blue
   0 5		3 Green
   0 4		3 Red
   0 3		4 Blue
   0 2		4 Green
   0 1		4 Red
   0 0		5 Blue

   0 7		5 Green
   0 6		5 Red
   0 5		6 Blue
   0 4		6 Green
   0 3		6 Red
   0 2		7 Blue
   0 1		7 Green
   0 0		7 Red
