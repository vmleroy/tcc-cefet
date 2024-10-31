# This generator program expands a low-dimentional latent vector into a 2D array of tiles.
# Each line of input should be an array of z vectors (which are themselves arrays of floats -1 to 1)
# Each line of output is an array of 32 levels (which are arrays-of-arrays of integer tile ids)

import argparse
import os
import numpy
import typing

import torch
import torchvision.utils as vutils
from torch.autograd import Variable

import models.dcgan as dcgan
from mario.pipes import calculate_pipe_fitness, find_pipes, get_pipes_positions, PipeTokens

parser = argparse.ArgumentParser()
parser.add_argument('--game', help='The game to generate samples on', choices=['mario', 'zelda'])
parser.add_argument('--tiles', type=int, default=10, help='The number of tiles in the game')
parser.add_argument('--modelToLoad', default=32, help='The object to load the generator from')
parser.add_argument('--experiment', help='Where to store the result of the experiment')
parser.add_argument('--batchSize', type=int, default=1, help='Batch size (number of levels that are generated at once)')
parser.add_argument('--nz', type=int, default=32, help='size of the latent z vector')
parser.add_argument('--ngf', type=int, default=64)
parser.add_argument('--n_extra_layers', type=int, default=0)

opt = parser.parse_args()

testing_generator = False

ngpu = 1 # number of GPUs to use
image_size = 32 # size of the image
n_levels = opt.batchSize # number of levels to generate

game = opt.game # game to generate samples on
tiles = opt.tiles # number of tiles in the game
model = opt.modelToLoad # object to load the generator from
experiment = opt.experiment # where to store the result of the experiment

nz = opt.nz # size of the latent z vector
ngf = opt.ngf # number of features
n_extra_layers = opt.n_extra_layers # number of extra layers

if not experiment or not model:
    exit('Please specify an experiment and an object to generate')
if not game:
    exit('Please specify a game to generate samples on')
    
if not os.path.exists(experiment):
    exit('Experiment does not exist')
if not os.path.exists(f"{experiment}/pths/{model}"):
    exit('Model does not exist')
if not os.path.exists(f"{experiment}/generator_results"):
    os.makedirs(f"{experiment}/generator_results")

# Load the generator
generator = dcgan.DCGAN_G(image_size, nz, tiles, ngf, ngpu, n_extra_layers)
generator.load_state_dict(torch.load(f"{experiment}/pths/{model}", map_location=lambda storage, loc: storage, weights_only=True))

map_cut = [28, 14] if game == 'mario' else [16, 11]

# testing the generator to check if it is working
if testing_generator:
    noise = torch.FloatTensor(n_levels, nz, 1, 1).normal_(0, 1)
    with torch.no_grad():
        noise = Variable(noise)
        
    fake = generator(noise)

    im = fake.data.cpu().numpy()
    im = im[:, :, :map_cut[1], :map_cut[0]] #Cut of rest to fit the 14x28 tile dimensions
    im = numpy.argmax(im, axis=1)

    for i, img in enumerate(im):
        pipes = find_pipes(img)
        pipe_fitness = calculate_pipe_fitness(level=img, data_pipes={
            'max_pipes': 2,
            'alpha': 0.2,
            'min_pipes': 1,
            'beta': 0.2
        })
        pipes_positions = get_pipes_positions(pipes)
        # for pipe in pipes_positions:
        #     print(pipe)

        print(f"Level {i + 1}:")
        for index_row, row in enumerate(img):
            for index_column, column in enumerate(row):
                if column in PipeTokens.values():
                    if {'x': index_column, 'y': index_row, 'value': column} in pipes_positions:
                        print(f"\x1b[32m{column}\x1b[0m", end=' ')
                    else:
                        print(f"\x1b[31m{column}\x1b[0m", end=' ')
                else:
                    print(column, end=' ')  
            print()
        print(f"Pipes: {len(pipes)}")
        print(f"Pipe fitness: {pipe_fitness}")
        # for pipe in pipes:
        #     print(f"Pipe {pipe.id}: {pipe.height}")        
        print()
    
    exit()
    
'''
Selection of the best levels from the generator
- Variables:
    - [x] n_levels: number of levels to generate
    - fitness: list of fitness values for each level
    - best_levels: list of the best levels
- Algorithm:
    - [x] Generate n_levels levels
    - Calculate the fitness of each level
    - Select the best levels
'''
noise = torch.FloatTensor(n_levels, nz, 1, 1).normal_(0, 1)
with torch.no_grad():
    noise = Variable(noise)
    
fake = generator(noise)
im = fake.data.cpu().numpy()
im = im[:, :, :map_cut[1], :map_cut[0]] #Cut of rest to fit the 14x28 tile dimensions
im = numpy.argmax(im, axis=1)

MapFitness2D = typing.TypedDict('MapFitness2D', {'id': int, 'level': numpy.ndarray, 'fitness': float})
map_fitness: list[MapFitness2D] =  []
for i, img in enumerate(im):
    pipe_fitness = calculate_pipe_fitness(level=img, 
        data_pipes={
            'max_pipes': 2,
            'alpha': 0.2,
            'min_pipes': 1,
            'beta': 0.2
        }, 
        data_wrong_placement={
            'gama': 0.2
        })
    map_fitness.append({'id': i, 'level': img, 'fitness': pipe_fitness})

map_fitness = sorted(map_fitness, key=lambda x: x['fitness'])
best_maps = map_fitness[:10]

for index, i in enumerate(best_maps):
    pipes = find_pipes(i['level'])
    pipes_positions = get_pipes_positions(pipes)
    
    print(f"Level {index} - id:{i['id']}:")
    for index_row, row in enumerate(i['level']):
        for index_column, column in enumerate(row):
            if column in PipeTokens.values():
                if {'x': index_column, 'y': index_row, 'value': column} in pipes_positions:
                    print(f"\x1b[32m{column}\x1b[0m", end=' ')
                else:
                    print(f"\x1b[31m{column}\x1b[0m", end=' ')
            else:
                print(column, end=' ')   
        print()
    print(f"Pipes: {len(pipes)}")
    print(f"Fitness: {i['fitness']}")
    print()


    
    
    
            




