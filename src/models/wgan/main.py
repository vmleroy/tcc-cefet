import keras
import sklearn 
import os

from critic import WganCritic
from generator import WganGenerator
from utils import *

latent_dim = 10 # 10 for zelda, 5 for mario
n_blocks = 10 # 3 for zelda, 10 for mario

batch_size = 16
n_steps = 1000
n_steps_critic = 100

critic = WganCritic(input_shape=(32, 32, n_blocks), batch_size=batch_size)
generator = WganGenerator(output_shape=(32, 32, n_blocks), latent_dim=latent_dim, batch_size=batch_size)

# Y = np.ones((batch_size, 1))
# X = np.random.randn(batch_size * latent_dim)

print('\n\n')

game_dir = os.path.join(os.getcwd(), 'src/data/mario-samples/translated-samples')
dataset, labels = load_real_samples(game_dir, n_blocks)
labels = label_encoding(labels)

num_batches = dataset.shape[0] / batch_size
X_real, Y_real = generate_real_samples(dataset, batch_size)
print('X_real', X_real.shape, 'Y_real', Y_real.shape)
print('X_real_example', X_real[0])
X_fake, Y_fake = generate_fake_samples(generator, latent_dim, batch_size)
print('X_fake', X_fake.shape, 'Y_fake', Y_fake.shape)

critic_loss, critic_accuracy = list(), list()
generator_loss, generator_accuracy = list(), list()
for i in range(n_steps):
  for _ in range(n_steps_critic):
    X_real, Y_real = generate_real_samples(dataset, batch_size)
    X_fake, Y_fake = generate_fake_samples(generator, latent_dim, batch_size)
    d_loss1 = critic.model.train_on_batch(X_real, Y_real)
    d_loss2 = critic.model.train_on_batch(X_fake, Y_fake)
    d_loss = 0.5 * np.add(d_loss1, d_loss2)
    critic_loss.append(d_loss)
    critic_accuracy.append(0.5 * np.add(d_loss1, d_loss2))

  # X_gan = generate_latent_points(latent_dim, batch_size)
  # Y_gan = -np.ones((batch_size, 1))
  # g_loss = gan.train_on_batch(X_gan, Y_gan)
  # generator_loss.append(g_loss)
  # generator_accuracy.append(g_loss)

  # print(f'Epoch: {i}, Critic Loss: {d_loss}, Generator Loss: {g_loss}')
