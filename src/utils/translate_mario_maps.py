import numpy, imageio, os

img_path = 'src/assets/'
maps_path = 'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/generator_results/v3_60s-samples_120s-levels'

complete_gan_all_samples = 'gan_generated_complete_levels_all_samples'
complete_gan_winnable_samples = 'gan_generated_complete_levels_winnable_samples'

complete_selection_all_samples = 'complete_levels_all_samples'
complete_selection_winnable_samples = 'complete_levels_winnable_samples'

map_size = (28 * 10 * 16, 14 * 16)

gan_maps = {
  'easy': {
    'all_samples': {
      'name': 'lvl_complete_51_map',
      'map': '',
    },
    'winnable_samples': {
      'name': 'lvl_complete_91_map',
      'map': '',
    },
  },
  'medium': {
    'all_samples': {
      'name': 'lvl_complete_20_map',
      'map': '',
    },
    'winnable_samples': {
      'name': 'lvl_complete_84_map',
      'map': '',
    },
  },
  'hard': {
    'all_samples': {
      'name': 'lvl_complete_152_map',
      'map': '',
    },
    'winnable_samples': {
      'name': 'lvl_complete_52_map',
      'map': '',
    },
  }
}

selection_maps = {
  'easy': {
    'all_samples': {
      'name': 'lvl_complete_0_map',
      'map': '',
    },
    'winnable_samples': {
      'name': 'lvl_complete_51_map',
      'map': '',
    },
  },
  'medium': {
    'all_samples': {
      'name': 'lvl_complete_19_map',
      'map': '',
    },
    'winnable_samples': {
      'name': 'lvl_complete_34_map',
      'map': '',
    },
  },
  'hard': {
    'all_samples': {
      'name': 'lvl_complete_4_map',
      'map': '',
    },
    'winnable_samples': {
      'name': 'lvl_complete_50_map',
      'map': '',
    },
  }
}

for key in gan_maps:
  with open(f'{maps_path}/{complete_gan_all_samples}/{gan_maps[key]["all_samples"]["name"]}.txt', 'r') as file:
    FILE = file.read()
    gan_maps[key]['all_samples']['map'] = FILE
  with open(f'{maps_path}/{complete_gan_winnable_samples}/{gan_maps[key]["winnable_samples"]["name"]}.txt', 'r') as file:
    FILE = file.read()
    gan_maps[key]['winnable_samples']['map'] = FILE
    
for key in selection_maps:
  with open(f'{maps_path}/{complete_selection_all_samples}/{selection_maps[key]["all_samples"]["name"]}.txt', 'r') as file:
    FILE = file.read()
    selection_maps[key]['all_samples']['map'] = FILE
  with open(f'{maps_path}/{complete_selection_winnable_samples}/{selection_maps[key]["winnable_samples"]["name"]}.txt', 'r') as file:
    FILE = file.read()
    selection_maps[key]['winnable_samples']['map'] = FILE
    
print(gan_maps)

spritesheet = (16, 16)
mapsheet = {
  "X": (1, 0),
  "S": (1, 6),
  "-": (2, 5),
  "?": (0, 1),
  "Q": (6, 1),
  "<": (2, 2),
  ">": (2, 3),
  "[": (2, 4),
  "]": (2, 5),
}
enemysheet = {
  'E': (0, 5)
}