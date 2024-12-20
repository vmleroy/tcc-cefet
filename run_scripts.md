# Examples of algorithm executions

## Generate samples

- python3 src/utils/database-creation.py --game=mario

## WGAN - DahstuhlGan

- python3 src/models/DagstuhlGAN/main.py --nz=32 --ngf=64 --ndf=64 --cuda --tiles=13 --json=src/data/mario/mario_levels_gamegan.json --experiment='src/data/mario/results/db-gamegan_nz-5_tiles-13_ngf-64_ndf-64_wgan-dagstuhl_v-1'

## WGAN -- Mine

- python3 src/models/MyWGAN/main.py --nz=32 --ngf=64 --ndf=64 --cuda --tiles=10 --dataset=src/data/mario/unified_samples.json --experiment='src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2'
- python3 src/models/MyWGAN/main.py --nz=32 --ngf=64 --ndf=64 --cuda --tiles=10 --dataset=src/data/zelda/unified_samples.json --experiment='src/data/zelda/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2'

## Generation -- Mine

- python3 src/models/MyWGAN/generate.py --experiment=src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2 --game=mario --tiles=10 --batchSize=1000 --modelToLoad=netG_epoch_77500_32.pth

## Mario AI

- /usr/bin/env /usr/lib/jvm/java-11-openjdk-amd64/bin/java -cp /home/victor/.config/Code/User/workspaceStorage/3c9bc8e5720ecb564e00f004aa211ee6/redhat.java/jdt_ws/tcc-cefet_9881cbcc/bin PlayLevel -directory src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/ -ai default -execution samples
