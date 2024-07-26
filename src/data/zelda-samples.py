import os

zelda_dir = os.path.join(os.getcwd(), 'vglc', 'zelda')
zelda_maps = os.listdir(zelda_dir)
max_size = (11, 16)

xy_visited = []
rooms = []

def get_room(map_file, x, y):
  room = []
  for y_room in range(0, max_size[1]):
    room.append(map_file[y + y_room][x:x + max_size[0]])
    for x_room in range(0, max_size[0]):
      xy_visited.append((x + x_room, y + y_room))
  rooms.append(room)

def remove_duplicates(lst):
  return [list(t) for t in set(tuple(element) for element in lst)]

def save_room_file(room, room_num):
  save_dir = os.path.join(os.getcwd(), 'zelda-samples', 'samples')
  if not os.path.exists(save_dir):
    os.makedirs(save_dir)
  with open(os.path.join(save_dir, f'room_{room_num}.txt'), 'w') as f:
    for row in room:
      f.write(''.join(row) + '\n')

for zelda_map in zelda_maps:
  if zelda_map.startswith('tloz'):
    with open(os.path.join(zelda_dir, zelda_map), 'r') as f:
      map_file = f.read()
      map_file = map_file.split('\n')
      for y, row in enumerate(map_file):
        for x, char in enumerate(row):
            if char == 'W':
              if (x, y) not in xy_visited:
                get_room(map_file, x, y)
    xy_visited = []

rooms = remove_duplicates(rooms)
for i, room in enumerate(rooms):
  save_room_file(room, i)