class Wgan:
  def __init__(self, generator, critic):
    self.generator = generator
    self.critic = critic