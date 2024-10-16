WGAN - DahstuhlGan
* python3 src/models/DagstuhlGAN/main.py --nz=32 --ngf=64 --ndf=64 --cuda --tiles=13 --json=src/data/mario/mario_levels_gamegan.json --experiment='src/data/mario/results/db-gamegan_nz-5_tiles-13_ngf-64_ndf-64_wgan-dagstuhl_v-1'

WGAN -- Mine
* python3 src/models/MyWassersteinGAN/main.py --nz=32 --ngf=64 --ndf=64 --cuda --tiles=13 --dataset=src/data/mario/mario_levels_gamegan.json --experiment='src/data/mario/results/db-gamegan_nz-5_tiles-13_ngf-64_ndf-64_wgan-mine_v-1'