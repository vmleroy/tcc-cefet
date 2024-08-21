import keras as k
from utils import wasserstein_loss

class WganCritic:
  model = k.models.Sequential()
  
  def __init__(self, batch_size, input_shape, learning_rate=0.00005):
    self.model.name = 'WganCritic'
    
    # Input layer -- must be the size of the image
    self.model.add(k.layers.InputLayer(shape=input_shape, batch_size=batch_size))
    
    # Convolutional layers
    self.model.add(k.layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same'))
    self.model.add(k.layers.LeakyReLU())
    self.model.add(k.layers.BatchNormalization())
    
    self.model.add(k.layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
    self.model.add(k.layers.LeakyReLU())
    self.model.add(k.layers.BatchNormalization())
    
    self.model.add(k.layers.Conv2D(256, (5, 5), strides=(2, 2), padding='same'))
    self.model.add(k.layers.LeakyReLU())
    self.model.add(k.layers.BatchNormalization())
    
    # Flatten the output
    self.model.add(k.layers.Flatten())
    
    # Output layer
    self.model.add(k.layers.Dense(1))
    
    optimizer = k.optimizers.RMSprop(learning_rate=learning_rate)
    self.model.compile(loss=wasserstein_loss, optimizer=optimizer)
    
    self.model.summary()
    
    