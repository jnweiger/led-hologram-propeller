blur=1x1
rm -rf blurred-out
mkdir -p blurred-out/{a,b,c,d,e,f}
for i in out/?/*.png; do
  convert $i -blur $blur blurred-$i
done
set -x
ffmpeg -framerate 20 -pattern_type glob -i 'blurred-out/*/*.png' -c:v libx264 -pix_fmt yuv420p fablabnbg_logo-20fps-b$blur.mp4
rm -rf blurred-out
