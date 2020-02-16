#! /bin/bash
# rm -rf out
# mkdir -p out/{a,b,c,d,e,f}
# cp logo/logo0{0*,1[01234]*,150}.png       out/a
# cp lab/lab0{15[123456789],1[6789]*}.png   out/b
# cp lab/lab00{[01234]*,50}.png             out/c
# cp nbg/nbg0{15[123456789],1[6789]*}.png   out/d
# cp nbg/nbg00{[01234]*,50}.png             out/e
# cp logo/logo0{15[123456789],1[6789]*}.png out/f

## # make a gifanim that loops forever: (loop=0 means forever!)
## does not work. It starts 100%CPU looping to connect to nonexistant localhost:6668 forever.
# convert -delay 5 -loop 0 out/*/*.png fablabnbg_logo_anim.gif
# 

ffmpeg -framerate 15 -pattern_type glob -i 'out/*/*.png' -c:v libx264 -pix_fmt yuv420p fablabnbg_logo.mp4

# rm -rf out
