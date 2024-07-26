import os

mario_dir = os.path.join(os.getcwd(), 'vglc', 'smb')
mario_levels = os.listdir(mario_dir)
max_size = (32, 14)

xy_visited = []
samples = []

def get_sample(level_file, x):
  sample = []
  for y_sample in range(0, max_size[1]):
    sample.append(level_file[y_sample][x:x + max_size[0]])
    for x_sample in range(0, max_size[0]):
      xy_visited.append((x + x_sample, y_sample))
  samples.append(sample)

def save_level_file(level, level_num):
  save_dir = os.path.join(os.getcwd(), 'mario-samples', 'samples')
  if not os.path.exists(save_dir):
    os.makedirs(save_dir)
  with open(os.path.join(save_dir, f'level_{level_num}.txt'), 'w') as f:
    for row in level:
      f.write(''.join(row) + '\n')        

for mario_level in mario_levels:
  if mario_level.startswith('mario'):
    with open(os.path.join(mario_dir, mario_level), 'r') as f:
      level_file = f.read()
      level_file = level_file.split('\n')
      for x, char in enumerate(level_file[0]):
        if (x, 0) not in xy_visited:
          get_sample(level_file, x)
    xy_visited = []
      
for i, sample in enumerate(samples):
  save_level_file(sample, i)  