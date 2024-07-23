import keras as k

class WganGenerator:
  model = k.models.Sequential()
  
  def __init__ (self, batch_size, latent_dim, output_shape):
    # Input layer
    self.model.add(k.layers.InputLayer(input_shape=(latent_dim,), batch_size=batch_size))
    self.model.add(k.layers.Reshape((1, 1, latent_dim)))
    
    # Dense layers
    self.model.add(k.layers.Conv2DTranspose(256, (4, 4), strides=(2, 2), padding='same'))
    self.model.add(k.layers.ReLU())
    self.model.add(k.layers.BatchNormalization())
    
    self.model.add(k.layers.Conv2DTranspose(128, (8, 8), strides=(2, 2), padding='same'))
    self.model.add(k.layers.ReLU())
    self.model.add(k.layers.BatchNormalization())
    
    self.model.add(k.layers.Conv2DTranspose(64, (16, 16), strides=(2, 2), padding='same'))
    self.model.add(k.layers.ReLU())
    self.model.add(k.layers.BatchNormalization())
    
    # Output layer
    self.model.add(k.layers.Conv2D(output_shape[-1], (32, 32), activation='tanh', padding='same'))    

    
    