import json
import numpy

def translate_to_original(src: str, level: numpy.ndarray):
  json_map_translate = json.load(open(src))
  
  translated_level = [[0 for _ in range(len(level[0]))] for _ in range(len(level))]
  
  for index_row, row in enumerate(level):
    for index_column, column in enumerate(row):
      for key, value in json_map_translate.items():
        if value == column:
          translated_level[index_row][index_column] = key
      
  return translated_level
