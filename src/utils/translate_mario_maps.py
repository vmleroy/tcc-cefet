import os
from PIL import Image

img_path = 'src/assets/'
maps_path = 'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/generator_results/v3_60s-samples_120s-levels'
save_path = f'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/maps'

complete_gan_all_samples = 'gan_generated_complete_levels_all_samples'
complete_gan_winnable_samples = 'gan_generated_complete_levels_winnable_samples'

complete_selection_all_samples = 'complete_levels_all_samples'
complete_selection_winnable_samples = 'complete_levels_winnable_samples'

sprite_size = (16, 16)
sample_size = (28, 14)
sample_quantity = 10
map_size = (sample_size[0] * sample_quantity * sprite_size[0], sample_size[1] * sprite_size[1])

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

assetsDir = os.listdir(img_path)
spriteList = {
  'mapsheet': Image.new('RGB', (0, 0), (255, 255, 255)),
  'enemysheet': Image.new('RGB', (0, 0), (255, 255, 255)),
}
for file in assetsDir:
  if 'mapsheet' in file:
    spriteList['mapsheet'] = Image.open(f'{img_path}{file}')
  elif 'enemysheet' in file:
    spriteList['enemysheet'] = Image.open(f'{img_path}{file}')

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

def create_map(map, name):
  map = map.split('\n')
  map = [list(row) for row in map]
  new_map = Image.new('RGB', map_size, (255, 255, 255))
  for y, row in enumerate(map):
    for x, tile in enumerate(row):
      if tile in mapsheet:
        sprite = spriteList['mapsheet'].crop((sprite_size[0] * mapsheet[tile][0], sprite_size[1] * mapsheet[tile][1], sprite_size[0] * (mapsheet[tile][0] + 1), sprite_size[1] * (mapsheet[tile][1] + 1)))
        new_map.paste(sprite, (x * sprite_size[0], y * sprite_size[1]))
      elif tile in enemysheet:
        sprite = spriteList['enemysheet'].crop((sprite_size[0] * enemysheet[tile][0], sprite_size[1] * enemysheet[tile][1], sprite_size[0] * (enemysheet[tile][0] + 1), sprite_size[1] * (enemysheet[tile][1] + 1)))
        new_map.paste(sprite, (x * sprite_size[0], y * sprite_size[1]))
  new_map.save(f'{save_path}/{name}.png')

if not os.path.exists(save_path):
  os.mkdir(save_path)

create_map(gan_maps['easy']['all_samples']['map'], f'gan_easy_all_samples__{gan_maps["easy"]["all_samples"]["name"]}')