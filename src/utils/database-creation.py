import os
import argparse

parser = argparse.ArgumentParser(description='Create a database from a directory of samples')
parser.add_argument('--game', help='The game to create a database for', choices=['zelda', 'mario'])
opt = parser.parse_args()

###
# ZELDA HELP FUNCTIONS
###
def generate_zelda_samples(files):
  width = 16
  height = 11
  
  for file in files:
    with open(file, 'r') as f:
      print(f'Processing {file}...')
      zelda_map = f.read().splitlines()
      
      print(f'File rows: {len(zelda_map)}, File columns: {len(zelda_map[0])}')
      file_count = 0
      
      rooms_per_width = int(len(zelda_map) / width)
      print(f'Rooms per width: {rooms_per_width}')
      rooms_per_height = int(len(zelda_map[0]) / height)
      print(f'Rooms per height: {rooms_per_height}')
      
      print('Generating samples...')
      
      for x in range(rooms_per_width):
        for y in range(rooms_per_height):          
          if (zelda_map[x * width][y * height] == '-'):
            print(f'\tRoom at ({x}, {y}) is empty')
            continue
          
          dir_name = f'src/data/zelda/samples'
          if not os.path.exists(os.path.dirname(dir_name)):
            os.mkdir(dir_name)
            
          file_path = f'{dir_name}/sample_{file.split("/")[-1].replace(".txt", "")}_{file_count}.txt'
          new_file = open(file_path, 'w')
          for i in range(width):
            row = []
            for j in range(height):              
              row.append(zelda_map[x * width + i][y * height + j])
            new_file.write(''.join(row) + '\n')
          new_file.close()
          file_count += 1
      
      print('Generated samples:', file_count)
      print()

###
# GENERAL HELP FUNCTIONS
###
def get_vglc_samples(dir_path, game):
  files = []
  for file in os.listdir(dir_path):
    if game == 'zelda' and file.endswith('.txt') and file.startswith('tloz'):
      files.append(f'src/data/{game}/vglc/{file}')
    elif game == 'mario' and file.endswith('.txt') and file.startswith('mario'):
      files.append(f'src/data/{game}/vglc/{file}')
  return files

def generate_samples (files, game):
  if game == 'zelda':
    return generate_zelda_samples(files)
      
game = opt.game
game_vglc_dir = f'src/data/{game}/vglc'    

files = get_vglc_samples(game_vglc_dir, game)
generate_samples(files, game)  