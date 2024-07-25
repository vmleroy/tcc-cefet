import keras

from critic import WganCritic
from generator import WganGenerator

batch_size = 1
critic_input_shape = (32, 32, 3)
samples_shape = (batch_size, 32, 32, 3)

critic_samples = keras.ops.ones(samples_shape)
generator_samples = keras.ops.ones((batch_size, 10))

print("\n\n\n")

print("================= PREVIEW =================")
print("Batch size: ", batch_size)
print("Critic input shape: ", critic_input_shape)
print("Generator input shape: ", generator_samples.shape)
print("Generator output shape: ", critic_input_shape)

print("\n\n\n")

print ("================= CRITIC =================")
critic = WganCritic(input_shape=critic_input_shape, batch_size=batch_size)
print(critic.model.summary())
critic.model(critic_samples)

print("\n\n\n")

print("================= GENERATOR =================")
generator = WganGenerator(output_shape=critic_input_shape, latent_dim=10, batch_size=batch_size)
print(generator.model.summary())
generator.model(generator_samples)