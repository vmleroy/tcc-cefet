import keras as k
from utils import wasserstein_loss

class WganGenerator:
  model = k.models.Sequential()
  
  def __init__ (self, batch_size, latent_dim, output_shape, learning_rate=0.00005):
    self.model.name = 'WganGenerator'
    self.batch_size = batch_size
    self.latent_dim = latent_dim
    self.output_shape = output_shape
    self.learning_rate = learning_rate

  def build_generator(self):
    # Input layer
    self.model.add(k.layers.InputLayer(shape=(self.latent_dim,), batch_size=self.batch_size))
    self.model.add(k.layers.Reshape((1, 1, self.latent_dim)))
    
    # Dense layers
    self.model.add(k.layers.Conv2DTranspose(256, (4, 4), strides=(4, 4), padding='same'))
    self.model.add(k.layers.ReLU())
    self.model.add(k.layers.BatchNormalization())
    
    self.model.add(k.layers.Conv2DTranspose(128, (8, 8), strides=(2, 2), padding='same'))
    self.model.add(k.layers.ReLU())
    self.model.add(k.layers.BatchNormalization())
    
    self.model.add(k.layers.Conv2DTranspose(64, (16, 16), strides=(2, 2), padding='same'))
    self.model.add(k.layers.ReLU())
    self.model.add(k.layers.BatchNormalization())
    
    # Output layer
    self.model.add(k.layers.Conv2DTranspose(self.output_shape[-1], (32, 32), strides=(2,2), activation='tanh', padding='same'))    
    
    # optimizer = k.optimizers.RMSprop(learning_rate=learning_rate)
    # self.model.compile(loss=wasserstein_loss, optimizer=optimizer)
  
    self.model.summary()    
    
    