import keras
import sklearn 

from critic import WganCritic
from generator import WganGenerator
from utils import *

batch_size = 16
latent_dim = 10

critic = WganCritic(input_shape=(32, 32, 3), batch_size=batch_size)
generator = WganGenerator(output_shape=(32, 32, 3), latent_dim=latent_dim, batch_size=batch_size)

Y = np.ones((batch_size, 1))
X = np.random.randn(batch_size * latent_dim)
