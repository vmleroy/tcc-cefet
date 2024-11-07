import numpy

from mario.pipes import calculate_pipe_fitness, ArgumentsForNumberOfPipes, ArgumentsForWrongPipesPlacement
from mario.enemies import calculate_enemies_fitness, ArgumentsForNumberOfEnemies, ArgumentsForWrongEnemiesPlacement
from mario.blocks import calculate_holes_fitness, ArgumentsForNumberOfHoles

data_pipes_max_min: ArgumentsForNumberOfPipes = {'max_pipes': 3, 'alpha': 0.2, 'min_pipes': 1, 'beta': 0.2}
data_pipes_wrong_placement: ArgumentsForWrongPipesPlacement = {'gama': 0.2}

data_enemies_max_min: ArgumentsForNumberOfEnemies = {'max_enemies': 4, 'alpha': 0.2, 'min_enemies': 2, 'beta': 0.2}
data_enemies_wrong_placement: ArgumentsForWrongEnemiesPlacement = {'gama': 0.2}

data_holes_max_min: ArgumentsForNumberOfHoles = {'max_holes': 2, 'alpha': 0.2, 'min_holes': 1, 'beta': 0.2}
  

def print_fitness_specs():
  print(f"Fitness specs:")
  print(f"  Enemies:")
  print(f"    data_enemies_max_min: {data_enemies_max_min}")
  print(f"    data_enemies_wrong_placement: {data_enemies_wrong_placement}")
  print(f"  Pipes:")
  print(f"    data_pipes_max_min: {data_pipes_max_min}")
  print(f"    data_pipes_wrong_placement: {data_pipes_wrong_placement}")
  print(f"  Holes:")
  print(f"    data_holes_max_min: {data_holes_max_min}")
  print()
    
def calculate_fitness(level: numpy.ndarray, print_specs: bool = False) -> float:
  pipe_fitness = calculate_pipe_fitness(
    level=level, 
    data_pipes=data_pipes_max_min, 
    data_wrong_placement=data_pipes_wrong_placement
  )
  enemies_fitness = calculate_enemies_fitness(
    level=level,
    data_enemies=data_enemies_max_min,
    data_wrong_placement=data_enemies_wrong_placement
  )
  hole_fitness = calculate_holes_fitness(
    level=level,
    data_holes=data_holes_max_min
  )
  return pipe_fitness + enemies_fitness + hole_fitness