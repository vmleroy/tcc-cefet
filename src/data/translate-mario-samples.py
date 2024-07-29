import os

mario_dir = os.path.join(os.getcwd(), 'mario-samples', 'expanded-samples')
mario_levels = os.listdir(mario_dir)

translate_dict = {
  'X': '0',
  'S': '1',
  '-': '2',
  '?': '3',
  'Q': '4',
  'E': '5',
  '<': '6',
  '>': '7',
  '[': '8',
  ']': '9',
  'o': '2',
  'B': '2',
  'b': '2',
}

save_dir = os.path.join(os.getcwd(), 'mario-samples', 'translated-samples')
if not os.path.exists(save_dir):
  os.makedirs(save_dir)

for mario_level in mario_levels:
  with open(os.path.join(mario_dir, mario_level), 'r') as f:
    level_file = f.read()
    level_file = level_file.split('\n')
    level = []
    for row in level_file:
      level.append([translate_dict[char] for char in row])
    with open(os.path.join(save_dir, mario_level), 'w') as f:
      for row in level:
        f.write(''.join(row) + '\n')