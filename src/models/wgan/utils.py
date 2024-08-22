import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

def wasserstein_loss(y_true, y_pred):
    return tf.reduce_mean(y_true * y_pred)

def one_hot_encode(y, n_classes):
    return np.eye(n_classes, dtype='uint8')[y]

def translate_one_hot_encoding(y):
    return np.argmax(y, axis=-1)



def generate_latent_points(latent_dim, batch_size):
    x_input = np.random.normal(0, 1, (batch_size, latent_dim))
    x_input = x_input.reshape(batch_size, latent_dim)
    return x_input
  
def generate_fake_samples(generator, latent_dim, batch_size):
    x_input = generate_latent_points(latent_dim, batch_size)
    X = generator.model.predict(x_input)
    y = np.ones((batch_size, 1))
    return X, y
  


def load_real_samples(dir):
    files = os.listdir(dir)
    files.sort()
    samples = []
    for file in files:
        with open(os.path.join(dir, file), 'r') as f:
            level = f.read().strip().splitlines()
        samples.append(np.array([list(row) for row in level]))  
    samples = np.array([np.array([np.array([int(char) for char in row]) for row in level]) for level in samples])
    return samples
    
def real_samples_one_hot_encoding(dataset, n_blocks):
    samples = one_hot_encode(dataset, n_blocks)
    return samples

def generate_real_samples(dataset, batch_size):
    ix = np.random.randint(0, dataset.shape[0], batch_size)
    X = dataset[ix]
    y = -np.ones((batch_size, 1))
    return X, y



def summarize_performance(step, generator, latent_dim, game_dir, n_samples=10):
    X, _ = generate_fake_samples(generator, latent_dim, n_samples)
    X = translate_one_hot_encoding(X)
    for index, generated in enumerate(X):
        with open(os.path.join(game_dir, f'generated_{step}_{index}.txt'), 'w') as f:
            for row in generated:
                f.write(''.join([str(char) for char in row]) + '\n')
    
def plot_history(c1_hist, c2_hist, g_hist):
    plt.plot(c1_hist, label='crit_real')
    plt.plot(c2_hist, label='crit_fake')
    plt.plot(g_hist, label='gen')
    plt.legend()
    plt.show()