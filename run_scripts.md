Generate samples
* python3 src/utils/database-creation.py --game=mario

WGAN - DahstuhlGan
* python3 src/models/DagstuhlGAN/main.py --nz=32 --ngf=64 --ndf=64 --cuda --tiles=13 --json=src/data/mario/mario_levels_gamegan.json --experiment='src/data/mario/results/db-gamegan_nz-5_tiles-13_ngf-64_ndf-64_wgan-dagstuhl_v-1'

WGAN -- Mine
* python3 src/models/MyWGAN/main.py --nz=32 --ngf=64 --ndf=64 --cuda --tiles=10 --dataset=src/data/mario/unified_samples.json --experiment='src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2'