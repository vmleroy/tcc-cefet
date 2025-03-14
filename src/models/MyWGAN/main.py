from __future__ import print_function
import os
import argparse
import random
import time
import math
import json

import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
from torch.autograd import Variable

import models.dcgan as dcgan

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default=None, help='Json file with example levels')
    parser.add_argument('--experiment', default=None, help='Where to store samples and models')
    parser.add_argument('--tiles', type=int, default=10, help='Number of tile types')
    
    parser.add_argument('--batchSize', type=int, default=32, help='input batch size')
    
    parser.add_argument('--nz', type=int, default=100, help='size of the latent z vector')
    parser.add_argument('--ngf', type=int, default=64)
    parser.add_argument('--ndf', type=int, default=64)
    parser.add_argument('--niter', type=int, default=5000, help='number of epochs to train for')
    parser.add_argument('--Diters', type=int, default=5, help='number of D iters per each G iter')
    parser.add_argument('--lrD', type=float, default=0.00005, help='learning rate for Critic, default=0.00005')
    parser.add_argument('--lrG', type=float, default=0.00005, help='learning rate for Generator, default=0.00005')    
    parser.add_argument('--beta1', type=float, default=0.5, help='beta1 for adam. default=0.5')
    
    parser.add_argument('--cuda'  , action='store_true', help='enables cuda')
    parser.add_argument('--ngpu'  , type=int, default=1, help='number of GPUs to use')
    
    parser.add_argument('--netG', default='', help="path to netG (to continue training)")
    parser.add_argument('--netD', default='', help="path to netD (to continue training)")
    
    parser.add_argument('--clamp_lower', type=float, default=-0.01)
    parser.add_argument('--clamp_upper', type=float, default=0.01)
    
    parser.add_argument('--n_extra_layers', type=int, default=0, help='Number of extra layers on gen and disc')
    parser.add_argument('--adam', action='store_true', help='Whether to use adam (default is rmsprop)')
    opt = parser.parse_args()
    print(opt)

    if opt.experiment is None:
        opt.experiment = 'samples'
    os.system('mkdir {0}'.format(opt.experiment))
    os.system('mkdir {0}/samples'.format(opt.experiment))
    os.system('mkdir {0}/samples_txt'.format(opt.experiment))
    os.system('mkdir {0}/pths'.format(opt.experiment))
    os.system('mkdir {0}/logs'.format(opt.experiment))

    opt.manualSeed = random.randint(1, 10000) # fix seed
    print("Random Seed: ", opt.manualSeed)
    random.seed(opt.manualSeed)
    torch.manual_seed(opt.manualSeed)

    cudnn.benchmark = True

    if torch.cuda.is_available() and not opt.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")
        
    map_size = 32
    
    if opt.dataset:
        dataset = opt.dataset
    else:
        dataset = "example.json"
        
    X = np.array ( json.load(open(dataset)) )
    print(X)
    print ("SHAPE ", X.shape) 
    
    z_dims = opt.tiles #Numer different title types
    num_batches = X.shape[0] / opt.batchSize

    X_onehot = np.eye(z_dims, dtype='uint8')[X]
    X_onehot = np.rollaxis(X_onehot, 3, 1)
    print ("SHAPE ",X_onehot.shape)    #(173, 14, 28, 16)

    X_train = np.zeros ( (X.shape[0], z_dims, map_size, map_size) )*2
    X_train[:, 2, :, :] = 1.0  #Fill with empty space
    #Pad part of level so its a square
    X_train[:X.shape[0], :, :X.shape[1], :X.shape[2]] = X_onehot

    ngpu = int(opt.ngpu)
    nz = int(opt.nz)
    ngf = int(opt.ngf)
    ndf = int(opt.ndf)
    n_extra_layers = int(opt.n_extra_layers)

    # custom weights initialization called on netG and netD
    def weights_init(m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            m.weight.data.normal_(0.0, 0.02)
        elif classname.find('BatchNorm') != -1:
            m.weight.data.normal_(1.0, 0.02)
            m.bias.data.fill_(0)

    netG = dcgan.DCGAN_G(map_size, nz, z_dims, ngf, ngpu, n_extra_layers)
    netG.apply(weights_init)
    if opt.netG != '': # load checkpoint if needed
        netG.load_state_dict(torch.load(opt.netG))
    print(netG)

    netD = dcgan.DCGAN_D(map_size, nz, z_dims, ndf, ngpu, n_extra_layers)
    netD.apply(weights_init)
    if opt.netD != '':
        netD.load_state_dict(torch.load(opt.netD))
    print(netD)


    input = torch.FloatTensor(opt.batchSize, z_dims, map_size, map_size)
    noise = torch.FloatTensor(opt.batchSize, nz, 1, 1)
    fixed_noise = torch.FloatTensor(opt.batchSize, nz, 1, 1).normal_(0, 1)
    one = torch.FloatTensor([1])
    mone = one * -1

    if opt.cuda:
        netD.cuda()
        netG.cuda()
        input = input.cuda()
        one, mone = one.cuda(), mone.cuda()
        noise, fixed_noise = noise.cuda(), fixed_noise.cuda()

    # setup optimizer
    if opt.adam:
        optimizerD = optim.Adam(netD.parameters(), lr=opt.lrD, betas=(opt.beta1, 0.999))
        optimizerG = optim.Adam(netG.parameters(), lr=opt.lrG, betas=(opt.beta1, 0.999))
    else:
        optimizerD = optim.RMSprop(netD.parameters(), lr = opt.lrD)
        optimizerG = optim.RMSprop(netG.parameters(), lr = opt.lrG)

    def tiles2image(tiles):
        return plt.get_cmap('rainbow')(tiles/float(z_dims))

    def combine_images(generated_images):
        num = generated_images.shape[0]
        width = int(math.sqrt(num))
        height = int(math.ceil(float(num)/width))
        shape = generated_images.shape[1:]
        image = np.zeros((height*shape[0], width*shape[1],shape[2]), dtype=generated_images.dtype)
        for index, img in enumerate(generated_images):
            i = int(index/width)
            j = index % width
            image[i*shape[0]:(i+1)*shape[0], j*shape[1]:(j+1)*shape[1]] = img
        return image

    errD_real_arr, errD_fake_arr, errD_epoch_arr, errG_epoch_arr, errD_gen_arr, errG_gen_arr = np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([])
    temp_errD_gen, temp_errG_gen = np.array([]), np.array([])
    time_start = time.time()
    gen_iterations = 0
    for epoch in range(opt.niter):
        #data_iter = iter(dataloader)        
        X_train = X_train[torch.randperm( len(X_train) )]
        
        temp_errD_epoch, temp_errG_epoch = np.array([]), np.array([])
        i = 0
        while i < num_batches: #while i < len(dataloader):
            ############################
            # (1) Update D network
            ###########################
            for p in netD.parameters(): # reset requires_grad
                p.requires_grad = True # they are set to False below in netG update

            # train the discriminator Diters times
            if gen_iterations < 25 or gen_iterations % 500 == 0:
                Diters = 100
            else:
                Diters = opt.Diters
                
            temp_errD_real, temp_errD_fake  = np.array([]), np.array([])
            j = 0
            while j < Diters and i < num_batches: #while j < Diters and i < len(dataloader):
                j += 1

                # clamp parameters to a cube
                for p in netD.parameters():
                    p.data.clamp_(opt.clamp_lower, opt.clamp_upper)
                
                data = X_train[i*opt.batchSize:(i+1)*opt.batchSize] #data = data_iter.next()
                i += 1

                # train with real
                real_cpu = torch.FloatTensor(data) #real_cpu, _ = data
                netD.zero_grad()
                # batch_size = real_cpu.size(0)

                if opt.cuda:
                    real_cpu = real_cpu.cuda()
                input.resize_as_(real_cpu).copy_(real_cpu)
                inputv = Variable(input)

                errD_real = netD(inputv)
                errD_real.backward(one)

                # train with fake
                noise.resize_(opt.batchSize, nz, 1, 1).normal_(0, 1)
                noisev = Variable(noise, volatile = True) # totally freeze netG
                fake = Variable(netG(noisev).data)
                inputv = fake
                errD_fake = netD(inputv)
                errD_fake.backward(mone)
                errD = errD_real - errD_fake
                optimizerD.step()
                
                temp_errD_fake = np.append(temp_errD_fake, errD_fake.cpu().data.numpy())
                temp_errD_real = np.append(temp_errD_real, errD_real.cpu().data.numpy())
        
            errD_fake_arr = np.append(errD_fake_arr, np.mean(temp_errD_fake))
            errD_real_arr = np.append(errD_real_arr, np.mean(temp_errD_real))

            ############################
            # (2) Update G network
            ###########################
            for p in netD.parameters():
                p.requires_grad = False # to avoid computation
            netG.zero_grad()
            # in case our last batch was the tail batch of the dataloader,
            # make sure we feed a full batch of noise
            noise.resize_(opt.batchSize, nz, 1, 1).normal_(0, 1)
            noisev = Variable(noise)
            fake = netG(noisev)
            errG = netD(fake)
            errG.backward(one)
            optimizerG.step()
            gen_iterations += 1

            print('[%d/%d][%d/%d][%d] Loss_D: %f Loss_G: %f Loss_D_real: %f Loss_D_fake %f'
                % (epoch, opt.niter, i, num_batches, gen_iterations,
                errD.data[0], errG.data[0], errD_real.data[0], errD_fake.data[0]))
            
            temp_errD_gen = np.append(temp_errD_gen, errD.cpu().data.numpy())
            temp_errG_gen = np.append(temp_errG_gen, errG.cpu().data.numpy())
            temp_errD_epoch = np.append(temp_errD_epoch, errD.cpu().data.numpy())
            temp_errG_epoch = np.append(temp_errG_epoch, errG.cpu().data.numpy())
            
            if gen_iterations % 500 == 0:
                fake = netG(Variable(fixed_noise, volatile=True))
                
                im = fake.data.cpu().numpy()                                
                im = combine_images( tiles2image( np.argmax( im, axis = 1) ) )
                plt.imsave('{0}/samples/fake_samples_{1}.png'.format(opt.experiment, gen_iterations), im)
                
                text_im = fake.data.cpu().numpy()
                text_im = np.argmax(text_im, axis = 1)                    
                for index, images in enumerate(text_im):
                    with open('{0}/samples_txt/fake_samples_{1}_{2}.txt'.format(opt.experiment, gen_iterations, index), 'w') as f:
                        for row in images:
                            for tile in row:
                                f.write(str(tile) + ' ')
                            f.write('\n')
                
                torch.save(netG.state_dict(), '{0}/pths/netG_epoch_{1}_{2}.pth'.format(opt.experiment, gen_iterations, opt.nz))

                errD_gen_arr = np.append(errD_gen_arr, np.mean(temp_errD_gen))
                errG_gen_arr = np.append(errG_gen_arr, np.mean(temp_errG_gen))         
                temp_errD_gen = np.array([])
                temp_errG_gen = np.array([])
            
        errD_epoch_arr = np.append(errD_epoch_arr, np.mean(temp_errD_epoch))
        errG_epoch_arr = np.append(errG_epoch_arr, np.mean(temp_errG_epoch))
        temp_errD_epoch = np.array([])
        temp_errG_epoch = np.array([])

        # do checkpointing
        # torch.save(netG.state_dict(), '{0}/netG_epoch_{1}.pth'.format(opt.experiment, epoch))
        # torch.save(netD.state_dict(), '{0}/netD_epoch_{1}.pth'.format(opt.experiment, epoch))
    
    time_end = time.time()

    errD_gen_arr = errD_gen_arr[~np.isnan(errD_gen_arr)]
    errG_gen_arr = errG_gen_arr[~np.isnan(errG_gen_arr)]
    errD_real_arr = errD_real_arr[~np.isnan(errD_real_arr)]
    errD_fake_arr = errD_fake_arr[~np.isnan(errD_fake_arr)]
    errD_epoch_arr = errD_epoch_arr[~np.isnan(errD_epoch_arr)]
    errG_epoch_arr = errG_epoch_arr[~np.isnan(errG_epoch_arr)]

    print('Time taken: ' + time.strftime("%H:%M:%S", time.gmtime(time_end - time_start)), '\n\n\n')
    print('Error D (real / fake): ', errD_real_arr, '\n', errD_fake_arr, '\n\n\n')
    print('Error D: ', errD_gen_arr, '\n\n\n')
    print('Error G: ', errG_gen_arr, '\n\n\n')
    print('Error D per Epoch: ', errD_epoch_arr, '\n\n\n')
    print('Error G per Epoch: ', errG_epoch_arr, '\n\n\n')

    '''
    # Discriminator x Generator loss per epoch
    '''
    plt.plot(errD_epoch_arr)
    plt.legend(['Discriminator'])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/discriminator_losses_per_epoch.png'.format(opt.experiment))
    plt.close()

    plt.plot(errG_epoch_arr)
    plt.legend(['Generator'])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/generator_losses_per_epoch.png'.format(opt.experiment))
    plt.close()

    plt.plot(errD_epoch_arr)
    plt.plot(errG_epoch_arr)
    plt.legend(['Discriminator', 'Generator'])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/discriminator_generator_losses_per_epoch.png'.format(opt.experiment))
    plt.close()

    '''
    # Discriminator x Generator loss per 500 generations
    '''
    plt.plot(errD_gen_arr)
    plt.legend(['Discriminator'])
    plt.xlabel('Generations / 500')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/discriminator_losses_per_500_gen.png'.format(opt.experiment))
    plt.close()

    plt.plot(errG_gen_arr)
    plt.legend(['Generator'])
    plt.xlabel('Generations / 500')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/generator_losses_per_500_gen.png'.format(opt.experiment))
    plt.close()

    plt.plot(errD_gen_arr)
    plt.plot(errG_gen_arr)
    plt.legend(['Discriminator', 'Generator'])
    plt.xlabel('Generations / 500')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/discriminator_generator_losses_per_500_gen.png'.format(opt.experiment))
    plt.close()

    '''
    # Discriminator loss (Real and Fake)
    '''
    plt.plot(errD_real_arr)
    plt.legend(['Real'])
    plt.xlabel('Generation')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/real_discriminator_losses_per_gen.png'.format(opt.experiment))
    plt.close()

    plt.plot(errD_fake_arr)
    plt.legend(['Fake'])
    plt.xlabel('Generation')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/fake_discriminator_losses_per_gen.png'.format(opt.experiment))
    plt.close()

    plt.plot(errD_real_arr)
    plt.plot(errD_fake_arr)
    plt.legend(['Real', 'Fake'])
    plt.xlabel('Generation')
    plt.ylabel('Loss')
    plt.savefig('{0}/logs/real_fake_discriminator_losses_per_gen.png'.format(opt.experiment))
    plt.close()

    with open('{0}/logs/params.txt'.format(opt.experiment), 'w') as f:
        for arg in vars(opt):
            f.write(arg + ': ' + str(getattr(opt, arg)) + '\n')
        f.write('\n\nTime taken: ' + time.strftime("%H:%M:%S", time.gmtime(time_end - time_start)))
