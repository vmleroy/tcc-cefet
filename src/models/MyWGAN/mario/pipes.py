import typing
import numpy

from .blocks import GroundBlocks

PipeTokens2D = typing.TypedDict('PipeTokens2D', {'top_left': int, 'top_right': int, 'bottom_left': int, 'bottom_right': int})
PipeTokens: PipeTokens2D = {
    'top_left': 6,
    'top_right': 7,
    'bottom_left': 8,
    'bottom_right': 9
  }

PipePositions2D = typing.TypedDict('PipePositions2D', {'x': int, 'y': int, 'value': int})

class Pipe():
  id:str = ''
  height:int = 0
  positions:list[PipePositions2D] = []
  
  def __init__(self, id:str):
    self.id = id
    self.height = 0
    self.positions = []


def find_pipes(level: numpy.ndarray) -> list[Pipe]:
  pipes: list[Pipe] = []
  visited: list[tuple[int, int]] = []
  
  level_height = len(level)
  level_width = len(level[0])

  for y in range(len(level)):
    for x in range(len(level[y])):
      # Detect the top of the pipe
      if x <= level_width-2 and level[y][x] == PipeTokens['top_left'] and level[y][x+1] == PipeTokens['top_right'] and (x, y) not in visited and (x+1, y) not in visited:
        pipe = Pipe(f"pipe_{len(pipes)}_x{x}_y{y}")
        pipe.height = 1
        pipe.positions.append({'x': x, 'y': y, 'value': level[y][x]})
        visited.append((x, y))
        pipe.positions.append({'x': x+1, 'y': y, 'value': level[y][x+1]})
        visited.append((x+1, y))
        
        # Detect the bottom of the pipe
        valid = True
        for i in range(y+1, level_height):
          if level[i][x] == PipeTokens['bottom_left'] and level[i][x+1] == PipeTokens['bottom_right'] and (x, i) not in visited and (x+1, i) not in visited:
            pipe.height += 1
            pipe.positions.append({'x': x, 'y': i, 'value': level[i][x]})
            visited.append((x, i))
            pipe.positions.append({'x': x+1, 'y': i, 'value': level[i][x+1]})
            visited.append((x+1, i))
            continue
          
          # If the pipe is placed on top of a block, we need to check if the pipe is valid
          # To be valid the pipe must be on top of a ground block of a breakable block
          if level[i][x] in GroundBlocks.values() and level[i][x+1] in GroundBlocks.values():
            break
          
          # If the pipe is placed on top of another block, we skip this pipe
          valid = False
          break
            
        # If the pipe is valid, check if the above blocks of pipes aren't pipe blocks
        # We have to check 4 blocks above the pipe to make sure the pipe is valid and the game can be played      
        if valid:
          for i in range(y-4, y, 1):
            if level[i][x] in GroundBlocks.values() and level[i][x+1] in GroundBlocks.values():
              break
            if level[i][x] in PipeTokens.values() or level[i][x+1] in PipeTokens.values():
              valid = False
              break
            
          if valid:
            pipes.append(pipe)            
  return pipes

def get_pipes_positions(pipes: list[Pipe]) -> list[PipePositions2D]:
  positions: list[PipePositions2D] = []
  for pipe in pipes:
    for position in pipe.positions:
      positions.append(position)
  return positions


'''
Fitness function for the pipes
1. Calculate max pipes in the level
2. Calculate min pipes in the level
3. Penalty for wrong placement of pipes or pipes blocks
'''
ArgumentsForNumberOfPipes = typing.TypedDict('ArgumentsForNumberOfPipes', {'max_pipes': int, 'alpha': float, 'min_pipes': int, 'beta': float})
StartDataForNumberOfPipes:ArgumentsForNumberOfPipes = {'max_pipes': 1, 'alpha': 0.2, 'min_pipes': 1, 'beta': 0.2}
ArgumentsForWrongPipesPlacement = typing.TypedDict('ArgumentsForWrongPipesPlacement', {'gama': float})
StartDataForWrongPipesPlacement:ArgumentsForWrongPipesPlacement = {'gama': 0.2}

def max_pipes_in_level(level:numpy.ndarray, max_pipes:int=1, alpha:float=0.2) -> float:
  pipes = find_pipes(level)
  n_pipes = len(pipes)
  if n_pipes >= max_pipes:
    return abs(n_pipes - max_pipes) * alpha
  return 0.0

def min_pipes_in_level(level:numpy.ndarray, min_pipes:int=1, beta:float=0.2) -> float:
  pipes = find_pipes(level)
  n_pipes = len(pipes)
  if n_pipes <= min_pipes:
    return abs(n_pipes - min_pipes) * beta
  return 0.0

def wrong_pipes_placement(level:numpy.ndarray, gama:float=0.2) -> float:
  pipes = find_pipes(level)
  pipes_positions = get_pipes_positions(pipes)
  value = 0.0
  for index_row, row in enumerate(level):
    for index_column, column in enumerate(row):
      if column in PipeTokens.values():
        if {'x': index_column, 'y': index_row, 'value': column} not in pipes_positions:
          value += gama
  return value

def calculate_pipe_fitness(level:numpy.ndarray, data_pipes:ArgumentsForNumberOfPipes=StartDataForNumberOfPipes, data_wrong_placement:ArgumentsForWrongPipesPlacement=StartDataForWrongPipesPlacement) -> float:
  return max_pipes_in_level(level, data_pipes['max_pipes'], data_pipes['alpha']) + min_pipes_in_level(level, data_pipes['min_pipes'], data_pipes['beta']) + wrong_pipes_placement(level, data_wrong_placement['gama'])
  