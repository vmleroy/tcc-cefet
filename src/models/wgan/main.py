import keras
import sklearn 
import os

from critic import WganCritic
from generator import WganGenerator
from utils import *

batch_size = 16
latent_dim = 10
n_steps = 1000
n_steps_critic = 100

critic = WganCritic(input_shape=(32, 32, 3), batch_size=batch_size)
generator = WganGenerator(output_shape=(32, 32, 3), latent_dim=latent_dim, batch_size=batch_size)

# Y = np.ones((batch_size, 1))
# X = np.random.randn(batch_size * latent_dim)

game_dir = os.path.join(os.getcwd(), 'src/data/mario-samples/translated-samples')
print('GAME DIR:', game_dir)
dataset = load_real_samples(game_dir)

# for step in range(n_steps):
#     # Update the critic
#     for _ in range(n_steps_critic):
#         X_real, Y_real = generate_real_samples(dataset, batch_size)
#         X_fake, Y_fake = generate_fake_samples(generator, latent_dim, batch_size)
#         c_loss_1 = critic.train_on_batch(X_real, Y_real)
#         c_loss_2 = critic.train_on_batch(X_fake, Y_fake)
        
#     X_gan = generate_latent_points(latent_dim, batch_size)
#     y_gan = -np.ones((batch_size, 1))
#     g_loss = generator.train_on_batch(X_gan, y_gan)
#     if step % 10 == 0:
#         print(f"Step: {step}")
#         print(f"Loss: {critic.loss}")
#         print(f"Accuracy: {critic.accuracy}")
#         print(f"Generator Loss: {generator.loss}")
#         print(f"Generator Accuracy: {generator.accuracy}")
#         print()
