import os

rooms_dir = os.path.join(os.getcwd(), 'zelda-samples', 'samples')
zelda_rooms = os.listdir(rooms_dir)

room_size = (11, 16)
expand_to = (32, 32)

def save_room_file(room, room_num):
  save_dir = os.path.join(os.getcwd(), 'zelda-samples', 'expanded-samples')
  if not os.path.exists(save_dir):
    os.makedirs(save_dir)
  with open(os.path.join(save_dir, f'room_{room_num}.txt'), 'w') as f:
    for row in room:
      f.write(''.join(row) + '\n')

for i, room in enumerate(zelda_rooms):
  with open(os.path.join(rooms_dir, room), 'r') as f:
    room_file = f.read()
    room_file = room_file.split('\n')
    new_room = [['-'] * expand_to[0] for _ in range(expand_to[1])]
    for y, row in enumerate(room_file):
      for x, char in enumerate(row):
        new_room[y + (expand_to[1] - room_size[1])][x] = char
    save_room_file(new_room, i)
    