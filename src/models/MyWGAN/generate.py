# This generator program expands a low-dimentional latent vector into a 2D array of tiles.
# Each line of input should be an array of z vectors (which are themselves arrays of floats -1 to 1)
# Each line of output is an array of 32 levels (which are arrays-of-arrays of integer tile ids)

import argparse
import os
import numpy

import torch
import torchvision.utils as vutils
from torch.autograd import Variable

import models.dcgan as dcgan

parser = argparse.ArgumentParser()
parser.add_argument('--game', help='The game to generate samples on', choices=['mario', 'zelda'])
parser.add_argument('--tiles', type=int, default=10, help='The number of tiles in the game')
parser.add_argument('--modelToLoad', default=32, help='The object to load the generator from')
parser.add_argument('--experiment', help='Where to store the result of the experiment')
parser.add_argument('--batchSize', type=int, default=1, help='Batch size')
parser.add_argument('--nz', type=int, default=32, help='size of the latent z vector')
parser.add_argument('--ngf', type=int, default=64)
parser.add_argument('--n_extra_layers', type=int, default=0)

opt = parser.parse_args()

testing_generator = True

imageSize = 32 # size of the image
ngpu = 1 # number of GPUs to use

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
generator = dcgan.DCGAN_G(imageSize, nz, tiles, ngf, ngpu, n_extra_layers)
generator.load_state_dict(torch.load(f"{experiment}/pths/{model}", map_location=lambda storage, loc: storage, weights_only=True))

map_cut = [28, 14] if game == 'mario' else [16, 11]

# testing the generator to check if it is working
if testing_generator:
    noise = torch.FloatTensor(opt.batchSize, nz, 1, 1).normal_(0, 1)
    with torch.no_grad():
        noise = Variable(noise)
        
    fake = generator(noise)

    im = fake.data.cpu().numpy()
    im = im[:, :, :map_cut[1], :map_cut[0]] #Cut of rest to fit the 14x28 tile dimensions
    im = numpy.argmax(im, axis=1)

    for i, img in enumerate(im):
        print(f"Level {i + 1}:")
        print(img)
        print()
    
    exit()




