import keras as k

from utils import wasserstein_loss

class Wgan:
  model = k.models.Sequential()
  def __init__(self, generator, critic, learning_rate=0.00005):
    self.model.name = 'Wgan'
    
    self.generator = generator.model
    self.critic = critic.model
    self.critic.trainable = False
    
    self.model.add(self.generator)
    self.model.add(self.critic)
    
    optimizer = k.optimizers.RMSprop(learning_rate=learning_rate)
    self.model.compile(loss=wasserstein_loss, optimizer=optimizer)
    
    self.model.summary()