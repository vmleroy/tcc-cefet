import os
import pprint
import typing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

Logs2D = typing.TypedDict('Logs2D', {
  'map_samples': typing.List[str],
  'game_status': str,
  'percentage_completion': str,
  'remaining_time': str,
  'elapsed_time': float,
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
  "SAMPLES": '-----------------------',
  "samples_in_level": 10,
  "total_samples": 0,
  "winnable_samples_percentage": 0.0,
  "WINNABLE_SAMPLES": '-----------------------',
  "total_levels_winnable_samples": 0,
  "levels_winnable_samples_percentage_based_on_samples": 0.0,
  "winnable_levels_percentage": 0.0,
  "ALL_SAMPLES": '-----------------------',
  "total_levels_all_samples": 0,
  "levels_all_samples_percentage_based_on_samples": 0.0,
  "winnable_levels_all_samples_percentage": 0.0,
  "STATISTICS": '-----------------------',
  'samples_statistics': {
    "elapsed_time": {
      "highest": 0,
      "lowest": 0,
      "mean": 0,
      "std_deviation": 0
    },
    "total_kills": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "jumps": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "difficulty": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
      "levels": {
      "easy (0.0 - 0.3)": 0,
      "medium (0.3 - 0.7)": 0,
      "hard (0.7 - 1.0)": 0
    },
  },
  'levels_winnable_samples_statistics': {
    "elapsed_time": {
      "highest": 0,
      "lowest": 0,
      "mean": 0,
      "std_deviation": 0
    },
    "total_kills": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "jumps": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "difficulty": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "levels": {
      "easy (0.0 - 0.3)": 0,
      "medium (0.3 - 0.7)": 0,
      "hard (0.7 - 1.0)": 0
    },
  },
  'levels_all_samples': {
    "elapsed_time": {
      "highest": 0,
      "lowest": 0,
      "mean": 0,
      "std_deviation": 0
    },
    "total_kills": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "jumps": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "difficulty": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "levels": {
      "easy (0.0 - 0.3)": 0,
      "medium (0.3 - 0.7)": 0,
      "hard (0.7 - 1.0)": 0
    },
  },
  "MAPS_LEVELS": '-----------------------',
  "samples_difficulty": [], 
  "levels_winnable_samples_difficulty": [],
  "levels_all_samples_difficulty": [],
}

selection_results = {
  "SAMPLES": '-----------------------',
  "samples_in_level": 10,
  "total_samples": 0,
  "winnable_samples_percentage": 0.0,
  "WINNABLE_SAMPLES": '-----------------------',
  "total_levels_winnable_samples": 0,
  "levels_winnable_samples_percentage_based_on_samples": 0.0,
  "winnable_levels_percentage": 0.0,
  "ALL_SAMPLES": '-----------------------',
  "total_levels_all_samples": 0,
  "levels_all_samples_percentage_based_on_samples": 0.0,
  "winnable_levels_all_samples_percentage": 0.0,
  "STATISTICS": '-----------------------',
  'samples_statistics': {
    "elapsed_time": {
      "highest": 0,
      "lowest": 0,
      "mean": 0,
      "std_deviation": 0
    },
    "total_kills": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "jumps": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "difficulty": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
      "levels": {
      "easy (0.0 - 0.3)": 0,
      "medium (0.3 - 0.7)": 0,
      "hard (0.7 - 1.0)": 0
    },
  },
  'levels_winnable_samples_statistics': {
    "elapsed_time": {
      "highest": 0,
      "lowest": 0,
      "mean": 0,
      "std_deviation": 0
    },
    "total_kills": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "jumps": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "difficulty": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "levels": {
      "easy (0.0 - 0.3)": 0,
      "medium (0.3 - 0.7)": 0,
      "hard (0.7 - 1.0)": 0
    },
  },
  'levels_all_samples': {
    "elapsed_time": {
      "highest": 0,
      "lowest": 0,
      "mean": 0,
      "std_deviation": 0
    },
    "total_kills": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "jumps": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "difficulty": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "levels": {
      "easy (0.0 - 0.3)": 0,
      "medium (0.3 - 0.7)": 0,
      "hard (0.7 - 1.0)": 0
    },
  },
  "MAPS_LEVELS": '-----------------------',
  "samples_difficulty": [], 
  "levels_winnable_samples_difficulty": [],
  "levels_all_samples_difficulty": [],
}


file_path = 'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/generator_results'
files_version = 'v3'



def convert_log (file, type = 'sample') -> Logs2D:
  object_logs: Logs2D = {
    'map_samples': [],
    'game_status': '',
    'percentage_completion': '',
    'remaining_time': '',
    'elapsed_time': 0.0,
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
          for sample in line.split(':')[1].split(','):
            object_logs['map_samples'].append(sample.strip())
        case string if string.find('Game Status') != -1:
          object_logs['game_status'] = line.split(':')[1].strip()
        case string if string.find('Percentage Completion') != -1:
          object_logs['percentage_completion'] = line.split(':')[1].strip()
        case string if string.find('Remaining Time') != -1:
          map_time = 60 if type == 'sample' else 120
          object_logs['remaining_time'] = line.split(':')[1].strip()
          object_logs['elapsed_time'] = map_time - int(line.split(':')[1].strip())
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
    if int(logs[key]['elapsed_time']) > highest_time:
      highest_time = int(logs[key]['elapsed_time'])
    if int(logs[key]['elapsed_time']) < lowest_time:
      lowest_time = int(logs[key]['elapsed_time'])
  return highest_time, lowest_time

def calculate_mean_and_std_deviation_time (logs: dict):
  sum_time = 0
  for key in logs:
    sum_time += int(logs[key]['elapsed_time'])
  mean_time = sum_time / len(logs)
  
  sum_time = 0
  for key in logs:
    sum_time += (int(logs[key]['elapsed_time']) - mean_time) ** 2
  std_deviation_time = (sum_time / len(logs)) ** 0.5
  return mean_time, std_deviation_time

def find_highest_and_lowest_kills (logs: dict):
  highest_kills = 0
  lowest_kills = 999999999
  for key in logs:
    if int(logs[key]['total_kills']) > highest_kills:
      highest_kills = int(logs[key]['total_kills'])
    if int(logs[key]['total_kills']) < lowest_kills:
      lowest_kills = int(logs[key]['total_kills'])
  return highest_kills, lowest_kills

def calculate_mean_and_std_deviation_kills (logs: dict):
  sum_kills = 0
  for key in logs:
    sum_kills += int(logs[key]['total_kills'])
  mean_kills = sum_kills / len(logs)
  
  sum_kills = 0
  for key in logs:
    sum_kills += (int(logs[key]['total_kills']) - mean_kills) ** 2
  std_deviation_kills = (sum_kills / len(logs)) ** 0.5
  return mean_kills, std_deviation_kills

def find_higher_and_lower_jumps(logs: dict):
  highest_jumps = 0
  lowest_jumps = 999999999
  for key in logs:
    if int(logs[key]['jumps']) > highest_jumps:
      highest_jumps = int(logs[key]['jumps'])
    if int(logs[key]['jumps']) < lowest_jumps:
      lowest_jumps = int(logs[key]['jumps'])
  return highest_jumps, lowest_jumps

def calculate_mean_and_std_deviation_jumps (logs: dict):
  sum_jumps = 0
  for key in logs:
    sum_jumps += int(logs[key]['jumps'])
  mean_jumps = sum_jumps / len(logs)
  
  sum_jumps = 0
  for key in logs:
    sum_jumps += (int(logs[key]['jumps']) - mean_jumps) ** 2
  std_deviation_jumps = (sum_jumps / len(logs)) ** 0.5
  return mean_jumps, std_deviation_jumps

def find_difficulty (logs: dict):
  result_logs = {}
  
  w_t = 0.3
  w_j = 0.3
  w_k = 0.4
  
  [highest_time, lowest_time] = find_highest_and_lowest_time(logs)
  [highest_kills, lowest_kills] = find_highest_and_lowest_kills(logs)
  [highest_jumps, lowest_jumps] = find_higher_and_lower_jumps(logs)

  for key in logs:
    normalized_time = (int(logs[key]['elapsed_time']) - lowest_time) / (highest_time - lowest_time)
    normalized_kills = (int(logs[key]['total_kills']) - lowest_kills) / (highest_kills - lowest_kills)
    normalized_jumps = (int(logs[key]['jumps']) - lowest_jumps) / (highest_jumps - lowest_jumps)
    
    # result_logs[key]['difficulty'] = (normalized_time * w_t) + (normalized_kills * w_k) + (normalized_jumps * w_j)
    # result_logs[key]['map_samples'] = logs[key]['map_samples']
    
    result_logs[key] = {
      'elapsed_time': logs[key]['elapsed_time'],
      'total_kills': logs[key]['total_kills'],
      'jumps': logs[key]['jumps'],
      'difficulty': (normalized_time * w_t) + (normalized_kills * w_k) + (normalized_jumps * w_j),
      # 'map_samples': logs[key]['map_samples']
    }
    
  return result_logs

def find_higher_and_lower_difficulty (logs: dict):
  highest_difficulty = 0
  lowest_difficulty = 999999999
  for key in logs:
    if logs[key]['difficulty'] > highest_difficulty:
      highest_difficulty = logs[key]['difficulty']
    if logs[key]['difficulty'] < lowest_difficulty:
      lowest_difficulty = logs[key]['difficulty']
  return highest_difficulty, lowest_difficulty

def calculate_mean_and_std_deviation_difficulty (logs: dict):
  sum_difficulty = 0
  for key in logs:
    sum_difficulty += logs[key]['difficulty']
  mean_difficulty = sum_difficulty / len(logs)
  
  sum_difficulty = 0
  for key in logs:
    sum_difficulty += (logs[key]['difficulty'] - mean_difficulty) ** 2
  std_deviation_difficulty = (sum_difficulty / len(logs)) ** 0.5
  return mean_difficulty, std_deviation_difficulty

def find_difficulty_levels (logs: dict):
  easy = 0
  medium = 0
  hard = 0
  for key in logs:
    if logs[key]['difficulty'] >= 0.0 and logs[key]['difficulty'] < 0.3:
      easy += 1
    elif logs[key]['difficulty'] >= 0.3 and logs[key]['difficulty'] < 0.7:
      medium += 1
    elif logs[key]['difficulty'] >= 0.7 and logs[key]['difficulty'] <= 1.0:
      hard += 1
  return easy, medium, hard

def find_winnable_percentage (logs: dict):
  winnable_samples = 0
  for key in logs:
    if logs[key]['game_status'] == 'WIN':
      winnable_samples += 1
  return winnable_samples / len(logs)



def calculate_statistics(logs: dict):
  
  filtered_winnable_logs = {
    key: logs[key] for key in logs if logs[key]['game_status'] == 'WIN'
  }
  
  result_logs = {
    "elapsed_time": {
      "highest": 0,
      "lowest": 0,
      "mean": 0,
      "std_deviation": 0
    },
    "total_kills": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "jumps": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "difficulty": {
      "highest": 0,
      "lowest": 0,
      "mean": 0.0,
      "std_deviation": 0.0
    },
    "levels": {
      "easy (0.0 - 0.3)": 0,
      "medium (0.3 - 0.7)": 0,
      "hard (0.7 - 1.0)": 0
    },
  }
  
  [highest_time, lowest_time] = find_highest_and_lowest_time(filtered_winnable_logs)
  [mean_time, std_deviation_time] = calculate_mean_and_std_deviation_time(filtered_winnable_logs)
  result_logs['elapsed_time']['highest'] = highest_time
  result_logs['elapsed_time']['lowest'] = lowest_time
  result_logs['elapsed_time']['mean'] = mean_time
  result_logs['elapsed_time']['std_deviation'] = std_deviation_time
  
  [highest_kills, lowest_kills] = find_highest_and_lowest_kills(filtered_winnable_logs)
  [mean_kills, std_deviation_kills] = calculate_mean_and_std_deviation_kills(filtered_winnable_logs)
  result_logs['total_kills']['highest'] = highest_kills
  result_logs['total_kills']['lowest'] = lowest_kills
  result_logs['total_kills']['mean'] = mean_kills
  result_logs['total_kills']['std_deviation'] = std_deviation_kills
  
  [highest_jumps, lowest_jumps] = find_higher_and_lower_jumps(filtered_winnable_logs)
  [mean_jumps, std_deviation_jumps] = calculate_mean_and_std_deviation_jumps(filtered_winnable_logs)
  result_logs['jumps']['highest'] = highest_jumps
  result_logs['jumps']['lowest'] = lowest_jumps
  result_logs['jumps']['mean'] = mean_jumps
  result_logs['jumps']['std_deviation'] = std_deviation_jumps
  
  logs_difficulty = find_difficulty(filtered_winnable_logs)
  [highest_difficulty, lowest_difficulty] = find_higher_and_lower_difficulty(logs_difficulty)
  [mean_difficulty, std_deviation_difficulty] = calculate_mean_and_std_deviation_difficulty(logs_difficulty)
  result_logs['difficulty']['highest'] = highest_difficulty
  result_logs['difficulty']['lowest'] = lowest_difficulty
  result_logs['difficulty']['mean'] = mean_difficulty
  result_logs['difficulty']['std_deviation'] = std_deviation_difficulty

  [easy, medium, hard] = find_difficulty_levels(logs_difficulty)
  result_logs['levels']['easy (0.0 - 0.3)'] = easy
  result_logs['levels']['medium (0.3 - 0.7)'] = medium
  result_logs['levels']['hard (0.7 - 1.0)'] = hard
  
  return result_logs

def get_data_to_histogram(logs: dict):
  logs_difficulty = find_difficulty(logs)
  
  jumps_values = [float(log['jumps']) for log in logs_difficulty.values()]
  enemies_killed_values = [float(log['total_kills']) for log in logs_difficulty.values()]
  difficulty_values = [float(log['difficulty']) for log in logs_difficulty.values()]
  time_values = [float(log['elapsed_time']) for log in logs_difficulty.values()]
  
  return {
    'jumps': jumps_values,
    'enemies_killed': enemies_killed_values,
    'difficulty': difficulty_values,
    'time': time_values
  }
  
def plot_histograms(logs: dict, path: str):
  histogram_data = get_data_to_histogram(logs)
  # Create subplots
  fig, axs = plt.subplots(2, 2, figsize=(12, 10))
  
  # Plot Jumps Histogram
  axs[0, 0].hist(histogram_data['jumps'], color='blue', alpha=0.7, density=True)
  axs[0, 0].set_title('Histogram of Jumps')
  axs[0, 0].set_xlabel('Number of Jumps')
  axs[0, 0].set_ylabel('Frequency')
  
  # Plot Kills Histogram
  axs[0, 1].hist(histogram_data['enemies_killed'], color='green', alpha=0.7, density=True)
  axs[0, 1].set_title('Histogram of Enemies Killed')
  axs[0, 1].set_xlabel('Number of Enemies Killed')
  axs[0, 1].set_ylabel('Frequency')
  
  # Plot Time Histogram
  axs[1, 0].hist(histogram_data['time'], color='orange', alpha=0.7, density=True)
  axs[1, 0].set_title('Histogram of Elapsed Time')
  axs[1, 0].set_xlabel('Elapsed Time (seconds)')
  axs[1, 0].set_ylabel('Frequency')
  
  # Plot Difficulty Histogram
  axs[1, 1].hist(histogram_data['difficulty'], color='purple', alpha=0.7, density=True)
  axs[1, 1].set_title('Histogram of Difficulty')
  axs[1, 1].set_xlabel('Difficulty Score')
  axs[1, 1].set_ylabel('Frequency')
  
  # Adjust layout
  plt.tight_layout()
    
  # Save the plot as an image
  plt.savefig(path)
  
def covariance_matrix(logs: dict, path: str):
  histogram_data = get_data_to_histogram(logs)
  x = np.ma.array([histogram_data['jumps'], histogram_data['enemies_killed'], histogram_data['difficulty'], histogram_data['time']])
  
  # Create a covariance matrix
  covariance_matrix = np.cov(x)
  
  # Add labels to the covariance matrix
  column_labels = ['Jumps', 'Enemies Killed', 'Difficulty', 'Time']
  row_labels = ['Jumps', 'Enemies Killed', 'Difficulty', 'Time']
  
  df = pd.DataFrame(covariance_matrix, columns=column_labels, index=row_labels)
  
  # Save the DataFrame to a CSV file
  df.to_csv(path, index=True)
  
def normalized_covariance_matrix(logs: dict, path: str):
  histogram_data = get_data_to_histogram(logs)
  x = np.ma.array([histogram_data['jumps'], histogram_data['enemies_killed'], histogram_data['difficulty'], histogram_data['time']])

  # Create a covariance matrix
  covariance_matrix = np.corrcoef(x)

  # Add labels to the normalized covariance matrix
  column_labels = ['Jumps', 'Enemies Killed', 'Difficulty', 'Time']
  row_labels = ['Jumps', 'Enemies Killed', 'Difficulty', 'Time']
  
  df = pd.DataFrame(covariance_matrix, columns=column_labels, index=row_labels)
  
  # Save the DataFrame to a CSV file
  df.to_csv(path, index=True)
  
def calculate_mann_whitney_u(logs_g1: dict, logs_g2: dict, path: str):
  logs_g1_data = get_data_to_histogram(logs_g1)
  logs_g2_data = get_data_to_histogram(logs_g2)
  
  # Perform the Mann-Whitney U test for all pairs of variables
  with open(path, 'w') as f:
    for key in logs_g1_data:
      u_statistic, p_value = stats.mannwhitneyu(logs_g1_data[key], logs_g2_data[key])
      f.write(f'Mann-Whitney U test for {key}:\n')
      f.write(f'U Statistic: {u_statistic}\n')
      f.write(f'P-Value: {p_value}\n\n')
  
  
  

for dir in os.listdir(file_path):
  if dir.startswith(files_version):
    for subDir in os.listdir(f'{file_path}/{dir}'):
      if subDir.startswith('gan'):
        match (subDir):
          case string if string.find('translated_logs') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              gan_generation_logs['samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}', 'sample')
                
          case string if string.find('all_samples') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              if (file.find('log') != -1):
                gan_generation_logs['levels_all_samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}', 'level')
                
          case string if string.find('winnable_samples') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              if (file.find('log') != -1):
                gan_generation_logs['levels_winnable_samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}', 'level')
      else:
        match (subDir):
          case string if string.find('translated_logs') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              selection_generation_logs['samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}', 'sample')
                
          case string if string.find('all_samples') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              if (file.find('log') != -1):
                selection_generation_logs['levels_all_samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}', 'level')
                
          case string if string.find('winnable_samples') != -1:
            for file in os.listdir(f'{file_path}/{dir}/{subDir}'):
              if (file.find('log') != -1):
                selection_generation_logs['levels_winnable_samples'][file] = convert_log(f'{file_path}/{dir}/{subDir}/{file}', 'level')

for key in gan_generation_logs:
  match (key):
    case 'samples':
      gan_results['total_samples'] = len(gan_generation_logs[key])
      gan_results['winnable_samples_percentage'] = find_winnable_percentage(gan_generation_logs[key])
      # gan_results['samples_difficulty'] = find_difficulty(gan_generation_logs[key])
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
      # selection_results['samples_difficulty'] = find_difficulty(selection_generation_logs[key])
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

gan_results['samples_statistics'] = calculate_statistics(gan_generation_logs['samples'])
gan_results['levels_winnable_samples_statistics'] = calculate_statistics(gan_generation_logs['levels_winnable_samples'])
gan_results['levels_all_samples'] = calculate_statistics(gan_generation_logs['levels_all_samples'])

selection_results['samples_statistics'] = calculate_statistics(selection_generation_logs['samples'])
selection_results['levels_winnable_samples_statistics'] = calculate_statistics(selection_generation_logs['levels_winnable_samples'])
selection_results['levels_all_samples'] = calculate_statistics(selection_generation_logs['levels_all_samples'])

print('GAN results:')
pprint.pp(gan_results)
print()
print('Selection results:')
pprint.pp(selection_results)    

# Generate histograms
histograms_folder = 'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/statistics/histograms'

all_samples_selection_histogram = plot_histograms(selection_generation_logs['levels_all_samples'], histograms_folder + '/all_samples_selection_histogram.png')
all_samples_gan_histogram = plot_histograms(gan_generation_logs['levels_all_samples'], histograms_folder + '/all_samples_gan_histogram.png')
winnable_samples_selection_histogram = plot_histograms(selection_generation_logs['levels_winnable_samples'], histograms_folder + '/winnable_samples_selection_histogram.png')
winnable_samples_gan_histogram = plot_histograms(gan_generation_logs['levels_winnable_samples'], histograms_folder + '/winnable_samples_gan_histogram.png')

# Save covariance matrices
covariance_matrices_folder = 'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/statistics/covariance_matrices'

all_samples_selection_covariance_matrix = covariance_matrix(selection_generation_logs['levels_all_samples'], covariance_matrices_folder + '/all_samples_selection_covariance_matrix.csv')
all_samples_gan_covariance_matrix = covariance_matrix(gan_generation_logs['levels_all_samples'], covariance_matrices_folder + '/all_samples_gan_covariance_matrix.csv')
winnable_samples_selection_covariance_matrix = covariance_matrix(selection_generation_logs['levels_winnable_samples'], covariance_matrices_folder + '/winnable_samples_selection_covariance_matrix.csv')
winnable_samples_gan_covariance_matrix = covariance_matrix(gan_generation_logs['levels_winnable_samples'], covariance_matrices_folder + '/winnable_samples_gan_covariance_matrix.csv')

# Save normalized covariance matrices
normalized_covariance_matrices_folder = 'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/statistics/normalized_covariance_matrices'

all_samples_selection_normalized_covariance_matrix = normalized_covariance_matrix(selection_generation_logs['levels_all_samples'], normalized_covariance_matrices_folder + '/all_samples_selection_normalized_covariance_matrix.csv')
all_samples_gan_normalized_covariance_matrix = normalized_covariance_matrix(gan_generation_logs['levels_all_samples'], normalized_covariance_matrices_folder + '/all_samples_gan_normalized_covariance_matrix.csv')
winnable_samples_selection_normalized_covariance_matrix = normalized_covariance_matrix(selection_generation_logs['levels_winnable_samples'], normalized_covariance_matrices_folder + '/winnable_samples_selection_normalized_covariance_matrix.csv')
winnable_samples_gan_normalized_covariance_matrix = normalized_covariance_matrix(gan_generation_logs['levels_winnable_samples'], normalized_covariance_matrices_folder + '/winnable_samples_gan_normalized_covariance_matrix.csv')

# Save Mann-Whitney U test results
mann_whitney_u_folder = 'src/data/mario/results/db-mine_nz-32_tiles-10_ngf-64_ndf-64_wgan-mine_v-2/statistics/mann_whitney_u'

mann_whitney_u_all_samples = calculate_mann_whitney_u(selection_generation_logs['levels_all_samples'], gan_generation_logs['levels_all_samples'], mann_whitney_u_folder + '/all_samples_selection_vs_gan.csv')
mann_whitney_u_winnable_samples = calculate_mann_whitney_u(selection_generation_logs['levels_winnable_samples'], gan_generation_logs['levels_winnable_samples'], mann_whitney_u_folder + '/winnable_samples_selection_vs_gan.csv')


        