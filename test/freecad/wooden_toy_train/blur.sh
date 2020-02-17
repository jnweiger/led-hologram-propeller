blur=1x1	# 2x2 is too much when rendering a 640 x 640 canvas.
rm -rf blurred-png
mkdir -p blurred-png
for i in png/*.png; do
  convert $i -blur $blur blurred-$i
done
set -x
ffmpeg -framerate 10 -pattern_type glob -i 'blurred-png/*.png' -c:v libx264 -pix_fmt yuv420p wooden_toy_train-10fps-b$blur.mp4
rm -rf blurred-out
