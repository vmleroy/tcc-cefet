import os
import numpy as np
import tensorflow as tf

def wasserstein_loss(y_true, y_pred):
    return tf.reduce_mean(y_true * y_pred)
  


def generate_latent_points(latent_dim, n_samples):
    x_input = np.random.randn(latent_dim * n_samples)
    x_input = x_input.reshape(n_samples, latent_dim)
    return x_input
  
def generate_fake_samples(generator, latent_dim, n_samples):
    x_input = generate_latent_points(latent_dim, n_samples)
    X = generator.predict(x_input)
    y = -np.ones((n_samples, 1))
    return X, y
  


def load_real_samples(game_dir):
    # import data from data directory representing the dataset
    files = os.listdir(game_dir)
    files.sort()
    samples = []
    for file in files:
        with open(os.path.join(game_dir, file), 'r') as f:
            sample = []
            for line in f:
                if line == '' or line == '\n':
                    continue
                line = line.removesuffix('\n').strip()
                aux = []
                for char in line:
                    aux.append(char)
                sample.append(aux)
        sample = np.array(sample)
        samples.append(sample)
    samples = np.array(samples)
    return samples
    
def generate_real_samples(dataset, n_samples):
    ix = np.random.randint(0, dataset.shape[0], n_samples)
    X = dataset[ix]
    y = np.ones((n_samples, 1))
    return X, y