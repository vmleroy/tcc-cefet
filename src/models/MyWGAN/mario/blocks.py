import typing
import numpy

EmptyTokens2D = typing.TypedDict('EmptyTokens2D', {'empty': int})
EmptyBlocks: EmptyTokens2D = {
    'empty': 2
}

SecretBlocks2D = typing.TypedDict('SecretBlocks2D', {'full': int, 'empty': int})
SecretBlocks: SecretBlocks2D = {
    'full': 3,
    'empty': 4
}

BreakableBlocks2D = typing.TypedDict('BreakableBlocks2D', {'breakable': int})
BreakableBlocks: BreakableBlocks2D = {
    'breakable': 1
}

GroundTokens2D = typing.TypedDict('GroundTokens2D', {'ground': int})
GroundBlocks: GroundTokens2D = {
    'ground': 0,
}

class Holes():
    id:str = ''
    size: int    
    position: list[tuple[int, int]]
    
    def __init__(self, id:str):
        self.id = id
        self.size = 0
        self.position = []

'''
Aux functions
'''
def find_holes(level:numpy.ndarray) -> list[Holes]:
  holes = []
  visited: list[tuple[int, int]] = []
  
  for x in range(len(level[-1])):
    # If the position is empty and it was not visited -- hole found
    if level[-1][x] == EmptyBlocks['empty'] and (x, len(level)-1) not in visited:
        hole = Holes(f"hole_{len(holes)}_x{x}_y{len(level)-1}")
        hole.size += 1
        hole.position.append((x, len(level)-1))
        visited.append((x, len(level)-1))

        # Check the size of the hole and if it is valid
        valid_hole = True
        for x_aux in range(x, len(level[-1])):     
          # If the next position is not empty, break the loop
          if level[len(level)-1][x_aux] != EmptyBlocks['empty']:
            break     
          # If the next position is empty, check the last 4 positions in Y axis
          for y in range(len(level) - 4, len(level)):
            # If the position is not empty, break the loop -- invalid hole
            if level[y][x_aux] != EmptyBlocks['empty']:
              valid_hole = False
              break
          # If the hole is not valid, break the loop
          if not valid_hole:
            break
          # If the hole is valid, add the position to the hole
          hole.size += 1
          hole.position.append((x_aux, len(level)-1))          
          visited.append((x_aux, len(level)-1))
        
        # If the hole is valid, add it to the list
        if valid_hole:
            holes.append(hole)
  return holes

def get_holes_positions(holes: list[Holes]) -> list[tuple[int, int]]:
  positions = []
  for hole in holes:
    positions += hole.position
  return positions

'''
Fitness functions
'''
ArgumentsForNumberOfHoles = typing.TypedDict('ArgumentsForNumberOfHoles', {'max_holes': int, 'alpha': float, 'min_holes': int, 'beta': float})
StartDataForNumberOfHoles:ArgumentsForNumberOfHoles = {'max_holes': 1, 'alpha': 0.2, 'min_holes': 1, 'beta': 0.2}

def max_holes_in_level(level:numpy.ndarray, max_holes:int=1, alpha:float=0.2) -> float:
  holes = find_holes(level)
  n_holes = len(holes)
  if n_holes >= max_holes:
    return abs(n_holes - max_holes) * alpha
  return 0.0

def min_holes_in_level(level:numpy.ndarray, min_holes:int=1, beta:float=0.2) -> float:
  holes = find_holes(level)
  n_holes = len(holes)
  if n_holes <= min_holes:
    return abs(n_holes - min_holes) * beta
  return 0.0

def calculate_holes_fitness(level:numpy.ndarray, data_holes:ArgumentsForNumberOfHoles=StartDataForNumberOfHoles) -> float:
  return max_holes_in_level(level, data_holes['max_holes'], data_holes['alpha']) + min_holes_in_level(level, data_holes['min_holes'], data_holes['beta'])