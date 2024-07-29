import os

rooms_dir = os.path.join(os.getcwd(), 'zelda-samples', 'expanded-samples')
zelda_rooms = os.listdir(rooms_dir)

translated_dir = {
  'F': '0',
  'W': '1',
  'B': '1',
  'D': '1',
  'S': '1',
  'M': '1',
  '-': '3',
  'P': '2',
  'O': '2',
  'I': '2',
}

save_dir = os.path.join(os.getcwd(), 'zelda-samples', 'translated-samples')
if not os.path.exists(save_dir):
  os.makedirs(save_dir)
  
for zelda_room in zelda_rooms:
  with open(os.path.join(rooms_dir, zelda_room), 'r') as f:
    room_file = f.read()
    room_file = room_file.split('\n')
    room = []
    for row in room_file:
      room.append([translated_dir[char] for char in row])
    with open(os.path.join(save_dir, zelda_room), 'w') as f:
      for row in room:
        f.write(''.join(row) + '\n')