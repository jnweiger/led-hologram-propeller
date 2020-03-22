set -x

# python3 encode_polar_bin.py ../test/freecad/four_primitives/t0*.png
# mv rgb_enc_01.bin four_prim_od.bin

env HOLO_REP_IMG=30 python3 encode_polar_bin.py ../test/png/arc_*shades.png
mv rgb_enc_01.bin arc_shades_od.bin
env HOLO_REP_IMG=30 python3 encode_polar_bin.py ../test/png/circ_grad_*.png
mv rgb_enc_01.bin circ_colors_od.bin
