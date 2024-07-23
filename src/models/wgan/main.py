import keras

import critic

input_shape = (16, 11, 3)

x = keras.ops.ones(input_shape)
y = critic.WganCritic(input_shape)

print(y.model.summary())

y.model(x)