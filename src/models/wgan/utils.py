import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

def wasserstein_loss(y_true, y_pred):
    return tf.reduce_mean(y_true * y_pred)
  
def label_encoding(labels):
    le = LabelEncoder()
    le.fit(labels)
    return le

def one_hot_encode(y, n_classes):
    return np.eye(n_classes, dtype='uint8')[y]



def generate_latent_points(latent_dim, n_samples):
    x_input = np.random.randn(latent_dim * n_samples)
    x_input = x_input.reshape(n_samples, latent_dim)
    return x_input
  
def generate_fake_samples(generator, latent_dim, n_samples):
    x_input = generate_latent_points(latent_dim, n_samples)
    X = generator.model.predict(x_input)
    y = np.ones((n_samples, 1))
    return X, y
  


def load_real_samples(game_dir, number_blocks=10):
    # import data from data directory representing the dataset
    files = os.listdir(game_dir)
    files.sort()
    samples = []
    labels = []
    for file in files:
        with open(os.path.join(game_dir, file), 'r') as f:
            sample = []
            for line in f:
                if line == '' or line == '\n':
                    continue
                line = line.removesuffix('\n').strip()
                aux = []
                for char in line:
                    char = int(char)
                    aux.append(char)
                    if char not in labels:
                        labels.append(char)
                sample.append(aux)
            sample = np.stack([sample] * number_blocks, axis=-1)
        samples.append(sample)
    samples = np.array(samples)
    return samples, labels
    
def generate_real_samples(dataset, n_samples):
    ix = np.random.randint(0, dataset.shape[0], n_samples)
    X = dataset[ix]
    y = -np.ones((n_samples, 1))
    return X, y



def summarize_performance(step, generator, latent_dim, n_blocks, game_dir, n_samples=10):
    X, _ = generate_fake_samples(generator, latent_dim, n_samples)
    X = np.argmax(X, axis=-1)
    with open(os.path.join(game_dir, step, f'generated.txt'), 'w') as f:
        for sample in X:
            for row in sample:
                f.write(''.join([str(x) for x in row]) + '\n')
            f.write('\n')
    
def plot_history(c1_hist, c2_hist, g_hist):
    plt.plot(c1_hist, label='crit_real')
    plt.plot(c2_hist, label='crit_fake')
    plt.plot(g_hist, label='gen')
    plt.legend()
    plt.show()