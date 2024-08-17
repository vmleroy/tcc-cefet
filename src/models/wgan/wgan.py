import keras as k

from utils import wasserstein_loss

class Wgan:
  model = k.models.Sequential()
  def __init__(self, generator, critic):
    self.generator = generator
    self.critic = critic
    self.critic.model.trainable = False
    
    self.model.add(self.generator.model)
    self.model.add(self.critic.model)
    
    optimizer = k.optimizers.RMSprop(learning_rate=0.00005)
    self.model.compile(loss=wasserstein_loss, optimizer=optimizer)