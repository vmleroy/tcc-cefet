import os
import argparse
import json

parser = argparse.ArgumentParser(description='Create a database from a directory of samples')
parser.add_argument('--game', help='The game to create a database for', choices=['zelda', 'mario'], default='mario')
opt = parser.parse_args()

##
# MARIO HELP FUNCTIONS
##
def generate_mario_samples(files):
  width = 28
  height = 14
  
  samples = []
  samples_count = 0
  

###
# ZELDA HELP FUNCTIONS
###
def generate_zelda_samples(files):
  width = 16
  height = 11
  
  samples = []
  samples_count = 0
  
  for file in files:
    with open(file, 'r') as f:
      print(f'Processing {file}...')
      zelda_map = f.read().splitlines()
      
      print(f'File rows: {len(zelda_map)}, File columns: {len(zelda_map[0])}')
      
      rooms_per_width = int(len(zelda_map) / width)
      print(f'Rooms per width: {rooms_per_width}')
      rooms_per_height = int(len(zelda_map[0]) / height)
      print(f'Rooms per height: {rooms_per_height}')
      
      print('Generating samples...')
      rooms_count = 0
      for x in range(rooms_per_width):
        for y in range(rooms_per_height):          
          if (zelda_map[x * width][y * height] == '-'):
            print(f'\tRoom at ({x}, {y}) is empty')
            continue
          print(f'\tRoom at ({x}, {y}) is not empty')

          # file_path = f'{dir_name}/sample_{file.split("/")[-1].replace(".txt", "")}_{file_count}.txt'
          # new_file = open(file_path, 'w')
          
          room = []
          for i in range(width):
            row = []
            for j in range(height):              
              row.append(zelda_map[x * width + i][y * height + j])
            room.append(row)
          samples.append(room)
          rooms_count += 1
      
    print('Generated samples:', rooms_count)
    samples_count += rooms_count
    print('Total samples:', samples_count)     
    print('Removing duplicates...')
    samples_no_duplicates = []
    for sample in samples:
      if sample not in samples_no_duplicates:
        samples_no_duplicates.append(sample)
    print('Removed duplicates:', len(samples_no_duplicates))
    print()
  
  print('Total samples:', len(samples_no_duplicates))
  print('Saving samples...')
  dir_name = 'src/data/zelda/samples'
  if not os.path.exists(dir_name):
    print('\tCreating directory:', dir_name)
    os.mkdir(dir_name)
    print('\tDirectory created')
  for i in range(len(samples_no_duplicates)):
    json_file = f'{dir_name}/sample_{i}.json'
    with open(json_file, 'w') as f:
      json.dump(samples_no_duplicates[i], f)
  print('Samples saved')
  print()
  

###
# GENERAL HELP FUNCTIONS
###
def get_vglc_samples(game_dir, game):
  files = []
  for file in os.listdir(os.path.join(game_dir, 'vglc')):
    if game == 'zelda' and file.endswith('.txt') and file.startswith('tloz'):
      files.append(f'src/data/{game}/vglc/{file}')
    elif game == 'mario' and file.endswith('.txt') and file.startswith('mario'):
      files.append(f'src/data/{game}/vglc/{file}')
  return files

def generate_samples (files, game):
  if game == 'zelda':
    return generate_zelda_samples(files)
  if game == 'mario':
    return generate_mario_samples(files)
  
def unify_and_translate_samples(game_dir):
  print('Loading samples...')
  samples = []
  for file in os.listdir(os.path.join(game_dir, 'samples')):
    with open(os.path.join(game_dir, 'samples', file), 'r') as f:
      samples.append(json.load(f))
  print('Total samples:', len(samples))
  print()
  
  game_translations = {}
  if game == 'zelda':
    game_translations = json.load(open(os.path.join(game_dir, 'zelda-to-rogue-tiles.json')))
  if game == 'mario':
    pass
  
  print('Translating samples...')
  translated_samples = []
  for sample in samples:
    translated_sample = []
    for row in sample:
      translated_row = []
      for tile in row:
        translated_row.append(game_translations[tile])
      translated_sample.append(translated_row)
    translated_samples.append(translated_sample)
  print('Samples translated')
  print()
  
  print('Saving unified samples at json...')
  json_file = os.path.join(game_dir, 'unified_samples.json')
  with open(json_file, 'w') as f:
    json.dump(translated_samples, f)    
  print('Unified samples saved at json')
  print()
  return samples
      
game = opt.game
game_dir = f'src/data/{game}'    
files = get_vglc_samples(game_dir, game)
generate_samples(files, game)  
unify_and_translate_samples(game_dir)
print('DONE!', 'Database created for', game)