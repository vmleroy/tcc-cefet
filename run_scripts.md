WGAN - Gamegan
* python3 src/models/GameGan/main.py --nz=5 --ngf=64 --ndf=64 --cuda --tiles=13 --json=src/data/mario/mario_levels_gamegan.json --experiment='src/data/mario/results/db-gamegan_nz-5_tiles-13_ngf-64_ndf-64_wgan-gamegan_v-1'

* python3 src/models/wgan/main.py --nz=10 --ngf=32 --ndf=32 --cuda --tiles=4 --json=src/data/zelda/unified_samples.json --experiment='src/data/zelda/results' --game='zelda'

WGAN - DahstuhlGan
* python3 src/models/DagstuhlGAN/main.py --nz=32 --ngf=64 --ndf=64 --cuda --tiles=13 --json=src/data/mario/mario_levels_gamegan.json --experiment='src/data/mario/results/db-gamegan_nz-5_tiles-13_ngf-64_ndf-64_wgan-dagstuhl_v-1'