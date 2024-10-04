WGAN
* python3 src/models/wgan/main.py  --nz=5 --ngf=64 --ndf=64 --cuda --tiles=10 --json=src/data/mario/unified_samples.json --experiment='src/data/mario/results_ngf64_ndf64_tiles10_mine'
* python3 src/models/wgan/main.py  --nz=5 --ngf=64 --ndf=64 --cuda --tiles=13 --json=src/data/mario/mario_levels_gamegan.json --experiment='src/data/mario/results/nz5_ngf64_ndf64_tiles13_gamegan'

* python3 src/models/wgan/main.py  --nz=10 --ngf=32 --ndf=32 --cuda --tiles=4 --json=src/data/zelda/unified_samples.json --experiment='src/data/zelda/results' --game='zelda'