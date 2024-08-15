import keras
import sklearn 
import os

from critic import WganCritic
from generator import WganGenerator
from wgan import Wgan
from utils import *

latent_dim = 5 # 10 for zelda, 5 for mario
n_blocks = 10 # 3 for zelda, 10 for mario

batch_size = 16
n_steps = 1000
n_steps_critic = 100

critic = WganCritic(input_shape=(32, 32, n_blocks), batch_size=batch_size)
generator = WganGenerator(output_shape=(32, 32, n_blocks), latent_dim=latent_dim, batch_size=batch_size)
wgan = Wgan(generator, critic)

# Y = np.ones((batch_size, 1))
# X = np.random.randn(batch_size * latent_dim)

print('\n\n')

game_dir = os.path.join(os.getcwd(), 'src/data/mario-samples/translated-samples')
dataset, labels = load_real_samples(game_dir, n_blocks)
labels = label_encoding(labels)

num_batches = dataset.shape[0] / batch_size
X_real, Y_real = generate_real_samples(dataset, batch_size)
print('X_real', X_real.shape, 'Y_real', Y_real.shape)
X_fake, Y_fake = generate_fake_samples(generator, latent_dim, batch_size)
print('X_fake', X_fake.shape, 'Y_fake', Y_fake.shape)

critic_loss_hist_1, critic_loss_hist_2 = list(), list()
generator_loss_hist = list()
for i in range(n_steps):
  # Update the critic more than the generator
  c_loss_1_temp, c_loss_2_temp = list(), list()
  for _ in range(n_steps_critic):
    X_real, Y_real = generate_real_samples(dataset, batch_size)
    X_fake, Y_fake = generate_fake_samples(generator, latent_dim, batch_size)
    c_loss_1 = critic.model.train_on_batch(X_real, Y_real)
    c_loss_2 = critic.model.train_on_batch(X_fake, Y_fake)
    c_loss_1_temp.append(c_loss_1)
    c_loss_2_temp.append(c_loss_2)
    
  critic_loss_hist_1.append(np.mean(c_loss_1_temp))
  critic_loss_hist_2.append(np.mean(c_loss_2_temp))  
  X_gan = generate_latent_points(latent_dim, batch_size)
  Y_gan = -np.ones((batch_size, 1))
  g_loss = wgan.model.train_on_batch(X_gan, Y_gan)
  generator_loss_hist.append(g_loss)
  if i % 50 == 0:
    print(f'Epoch {i+1}, Critic Loss: {critic_loss_hist_1[-1]}, {critic_loss_hist_2[-1]}, Generator Loss: {generator_loss_hist[-1]}')
