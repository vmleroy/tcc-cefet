import keras as k

class WganCritic:
  model = k.models.Sequential()
  
  def __init__(self, batch_size, input_shape):
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
    
    