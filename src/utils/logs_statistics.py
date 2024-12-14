import os
import pprint
import typing

Logs2D = typing.TypedDict('Logs2D', {
  'map_samples': typing.List[str],
  'game_status': str,
  'percentage_completion': str,
  'remaining_time': str,
  'lives': str,
  'coins': str,
  'mario_state': str,
  'total_kills': str,
  'bricks': str,
  'jumps': str,
  'max_x_jump': str,
  'max_air_time': str,
})

gan_generation_logs = {
  "samples": {},
  "levels_winnable_samples": {},
  "levels_all_samples": {}
}

selection_generation_logs = {
  "samples": {},
  "levels_winnable_samples": {},
  "levels_all_samples": {}
}

gan_results = {
  "samples_in_level": 10,
  
  "total_samples": 0,
  "winnable_samples_percentage": 0.0,
  "samples_difficulty": [], 
  
  "total_levels_winnable_samples": 0,
  "levels_winnable_samples_percentage_based_on_samples": 0.0,
  "winnable_levels_percentage": 0.0,
  "levels_winnable_samples_difficulty": [],
  
  "total_levels_all_samples": 0,
  "levels_all_samples_percentage_based_on_samples": 0.0,
  "winnable_levels_all_samples_percentage": 0.0,
  "levels_all_samples_difficulty": [],
}

selection_results = {
  "samples_in_level": 10,
  
  "total_samples": 0,
  "winnable_samples_percentage": 0.0,
  "samples_difficulty": [], 
  
  "total_levels_winnable_samples": 0,
  "levels_winnable_samples_percentage_based_on_samples": 0.0,
  "winnable_levels_percentage": 0.0,
  "levels_winnable_samples_difficulty": [],
  
  "total_levels_all_samples": 0,
  "levels_all_samples_percentage_based_on_samples": 0.0,
  "winnable_levels_all_samples_percentage": 0.0,
  "levels_all_samples_difficulty": [],
}


file_path = 'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/generator_results'
files_version = 'v3'



def convert_log (file):
  object_logs: Logs2D = {
    'map_samples': [],
    'game_status': '',
    'percentage_completion': '',
    'remaining_time': '',
    'lives': '',
    'coins': '',
    'mario_state': '',
    'total_kills': '',
    'bricks': '',
    'jumps': '',
    'max_x_jump': '',
    'max_air_time': '',
  }
  
  with open(file, 'r') as f:
    for line in f.readlines():
      match (line):
        case string if string.find('Map Samples') != -1:
          object_logs['map_samples'] = line.split(':')[1].strip().split(',')
        case string if string.find('Game Status') != -1:
          object_logs['game_status'] = line.split(':')[1].strip()
        case string if string.find('Percentage Completion') != -1:
          object_logs['percentage_completion'] = line.split(':')[1].strip()
        case string if string.find('Remaining Time') != -1:
          object_logs['remaining_time'] = line.split(':')[1].strip()
        case string if string.find('Lives') != -1:
          object_logs['lives'] = line.split(':')[1].strip()
        case string if string.find('Coins') != -1:
          object_logs['coins'] = line.split(':')[1].strip()
        case string if string.find('Mario State') != -1:
          object_logs['mario_state'] = line.split(':')[1].strip()
        case string if string.find('Total Kills') != -1:
          object_logs['total_kills'] = line.split(':')[1].strip()
        case string if string.find('Bricks') != -1:
          object_logs['bricks'] = line.split(':')[1].strip()
        case string if string.find('Jumps') != -1:
          object_logs['jumps'] = line.split(':')[1].strip()
        case string if string.find('Max X Jump') != -1:
          object_logs['max_x_jump'] = line.split(':')[1].strip()
        case string if string.find('Max Air Time') != -1:
          object_logs['max_air_time'] = line.split(':')[1].strip()
  
  return object_logs



def find_highest_and_lowest_time (logs: dict):
  highest_time = 0
  lowest_time = 999999999
  for key in logs:
    if int(logs[key]['remaining_time']) > highest_time:
      highest_time = int(logs[key]['remaining_time'])
    if int(logs[key]['remaining_time']) < lowest_time:
      lowest_time = int(logs[key]['remaining_time'])
  return highest_time, lowest_time

def find_highest_and_lowest_kills (logs: dict):
  highest_kills = 0
  lowest_kills = 999999999
  for key in logs:
    if int(logs[key]['total_kills']) > highest_kills:
      highest_kills = int(logs[key]['total_kills'])
    if int(logs[key]['total_kills']) < lowest_kills:
      lowest_kills = int(logs[key]['total_kills'])
  return highest_kills, lowest_kills

def find_difficulty (logs: dict):
  w_t = 0.5
  w_k = 0.5
  
  [highest_time, lowest_time] = find_highest_and_lowest_time(logs)
  [highest_kills, lowest_kills] = find_highest_and_lowest_kills(logs)

  for key in logs:
    normalized_time = (int(logs[key]['remaining_time']) - lowest_time) / (highest_time - lowest_time)
    normalized_kills = (int(logs[key]['total_kills']) - lowest_kills) / (highest_kills - lowest_kills)
    
    logs[key]['difficulty'] = (normalized_time * w_t) + (normalized_kills * w_k)
    
  return logs

def find_winnable_percentage (logs: dict):
  winnable_samples = 0
  for key in logs:
    if logs[key]['game_status'] == 'WIN':
      winnable_samples += 1
  return winnable_samples / len(logs)



for dir in os.listdir(file_path):
  if dir.startswith(files_version):
    for subDir in os.listdir(f'{file_path}/{dir}'):
      if subDir.startswith('gan'):
        match (subDir):
          case string if string.find('translated_logs') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              gan_generation_logs['samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}')
                
          case string if string.find('all_samples') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              if (file.find('log') != -1):
                gan_generation_logs['levels_all_samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}')
                
          case string if string.find('winnable_samples') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              if (file.find('log') != -1):
                gan_generation_logs['levels_winnable_samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}')
      else:
        match (subDir):
          case string if string.find('translated_logs') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              selection_generation_logs['samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}')
                
          case string if string.find('all_samples') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              if (file.find('log') != -1):
                selection_generation_logs['levels_all_samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}')
                
          case string if string.find('winnable_samples') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              if (file.find('log') != -1):
                selection_generation_logs['levels_winnable_samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}')

for key in gan_generation_logs:
  match (key):
    case 'samples':
      gan_results['total_samples'] = len(gan_generation_logs[key])
      gan_results['winnable_samples_percentage'] = find_winnable_percentage(gan_generation_logs[key])
      gan_results['samples_difficulty'] = find_difficulty(gan_generation_logs[key])
    case 'levels_winnable_samples':
      gan_results['total_levels_winnable_samples'] = len(gan_generation_logs[key])
      gan_results['levels_winnable_samples_percentage_based_on_samples'] = gan_results['total_levels_winnable_samples'] * gan_results['samples_in_level'] / gan_results['total_samples']
      gan_results['winnable_levels_percentage'] = find_winnable_percentage(gan_generation_logs[key])
      gan_results['levels_winnable_samples_difficulty'] = find_difficulty(gan_generation_logs[key])
    case 'levels_all_samples':
      gan_results['total_levels_all_samples'] = len(gan_generation_logs[key])
      gan_results['levels_all_samples_percentage_based_on_samples'] = gan_results['total_levels_all_samples'] * gan_results['samples_in_level'] / gan_results['total_samples']
      gan_results['winnable_levels_all_samples_percentage'] = find_winnable_percentage(gan_generation_logs[key])
      gan_results['levels_all_samples_difficulty'] = find_difficulty(gan_generation_logs[key])

for key in selection_generation_logs:
  match (key):
    case 'samples':
      selection_results['total_samples'] = len(selection_generation_logs[key])
      selection_results['winnable_samples_percentage'] = find_winnable_percentage(selection_generation_logs[key])
      selection_results['samples_difficulty'] = find_difficulty(selection_generation_logs[key])
    case 'levels_winnable_samples':
      selection_results['total_levels_winnable_samples'] = len(selection_generation_logs[key])
      selection_results['levels_winnable_samples_percentage_based_on_samples'] = selection_results['total_levels_winnable_samples'] * selection_results['samples_in_level'] / selection_results['total_samples']
      selection_results['winnable_levels_percentage'] = find_winnable_percentage(selection_generation_logs[key])
      selection_results['levels_winnable_samples_difficulty'] = find_difficulty(selection_generation_logs[key])
    case 'levels_all_samples':
      selection_results['total_levels_all_samples'] = len(selection_generation_logs[key])
      selection_results['levels_all_samples_percentage_based_on_samples'] = selection_results['total_levels_all_samples'] * selection_results['samples_in_level'] / selection_results['total_samples']
      selection_results['winnable_levels_all_samples_percentage'] = find_winnable_percentage(selection_generation_logs[key])
      selection_results['levels_all_samples_difficulty'] = find_difficulty(selection_generation_logs[key])

print('GAN results:')
pprint.pp(gan_results)
print()
print('Selection results:')
pprint.pp(selection_results)


      
        