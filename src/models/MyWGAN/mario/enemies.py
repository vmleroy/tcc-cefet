import typing
import numpy

from .blocks import EmptyBlocks

EnemiesTokens2D = typing.TypedDict('EnemiesTokens2D', {'goomba': int})
EnemiesTokens = {
    'goomba': 5,
}

class Enemies():
  id:str = ''
  name:str = ''
  position:tuple[int, int] 
  
  def __init__(self, id:str, name:str, position:tuple[int, int]):
    self.id = id
    self.name = name
    self.position = position
    
        
def find_enemies(level: numpy.ndarray) -> list[Enemies]:
    enemies: list[Enemies] = []
    visited: list[tuple[int, int]] = []
    
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == EnemiesTokens['goomba'] and (x, y) not in visited:
                enemy = Enemies(f"enemy_{len(enemies)}_x{x}_y{y}", 'goomba', (x, y))
                enemies.append(enemy)
                visited.append((x, y))
            
    return enemies

def get_enemies_positions(enemies: list[Enemies]):
    positions = []
    for enemy in enemies:
        positions.append(enemy.position)
        
    return positions

'''
Fitness function for the enemies
'''
ArgumentsForNumberOfEnemies = typing.TypedDict('ArgumentsForNumberOfEnemies', {'max_enemies': int, 'alpha': float, 'min_enemies': int, 'beta': float})
StartDataForNumberOfEnemies:ArgumentsForNumberOfEnemies = {'max_enemies': 1, 'alpha': 0.2, 'min_enemies': 1, 'beta': 0.2}

ArgumentsForWrongEnemiesPlacement = typing.TypedDict('ArgumentsForWrongEnemiesPlacement', {'gama': float})
StartDataForWrongEnemiesPlacement:ArgumentsForWrongEnemiesPlacement = {'gama': 0.2}

def max_enemies(level:numpy.ndarray, max_enemies:int=1, alpha:float=0.2) -> float:
    enemies = find_enemies(level)
    if len(enemies) >= max_enemies:
        return abs(len(enemies) - max_enemies) * alpha 
    return 0.0

def min_pipes_in_level(level:numpy.ndarray, min_enemies:int=1, beta:float=0.2) -> float:
    enemies = find_enemies(level)
    if len(enemies) <= min_enemies:
        return abs(len(enemies) - min_enemies) * beta
    return 0.0

def wrong_enemies_placement(level:numpy.ndarray, gama:float=0.2) -> float:
    enemies = find_enemies(level)
    value = 0.0
    for enemy in enemies:
        match enemy.name:
            case 'goomba':
                x, y = enemy.position
                if y > len(level) - 2 or level[y+1][x] in EmptyBlocks.values():
                    value += gama
                continue
            case _:
                pass
    return value

def calculate_enemies_fitness(level:numpy.ndarray, data_enemies:ArgumentsForNumberOfEnemies=StartDataForNumberOfEnemies, data_wrong_placement:ArgumentsForWrongEnemiesPlacement=StartDataForWrongEnemiesPlacement) -> float:
    return max_enemies(level, data_enemies['max_enemies'], data_enemies['alpha']) + min_pipes_in_level(level, data_enemies['min_enemies'], data_enemies['beta']) + wrong_enemies_placement(level, data_wrong_placement['gama'])