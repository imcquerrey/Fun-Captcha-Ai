from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import tensorflow as tf
import pickle
import time

# Loading Training Data
pickle_in = open("X.pickle","rb")
X = pickle.load(pickle_in)

pickle_in = open("y.pickle","rb")
y = pickle.load(pickle_in)

X = X/255.0

# Setting up different layers to test
dense_layers = [0, 1, 2]
layer_sizes = [32, 64, 128]
conv_layers = [1, 2, 3]
valdsplits = [0.1, 0.2, 0.3]

# Iterate over each different layer possibility
for dense_layer in dense_layers:
	for layer_size in layer_sizes:
		for conv_layer in conv_layers:
			for split in valdsplits:
				# Configuring name for current model
				NAME = "Captcha-{}-split-{}-conv-{}-nodes-{}-dense-{}".format(split, conv_layer, layer_size, dense_layer, int(time.time()))
				print(NAME)

				# Adding layers to the new model
				model = Sequential()

				model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:]))
				model.add(Activation('relu'))
				model.add(MaxPooling2D(pool_size=(2, 2)))

				for l in range(conv_layer-1):
					model.add(Conv2D(layer_size, (3, 3)))
					model.add(Activation('relu'))
				model.add(MaxPooling2D(pool_size=(2, 2)))

				model.add(Flatten())

				for _ in range(dense_layer):
					model.add(Dense(layer_size))
					model.add(Activation('relu'))

				model.add(Dense(1))
				model.add(Activation('sigmoid'))

				# Setting up the log so that it can be viewed on the tesorboard graph along with other trained models
				tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))

				model.compile(loss='binary_crossentropy',
							  optimizer='adam',
							  metrics=['accuracy'],
							  )

				# Starting to train the model
				model.fit(X, y,
						  batch_size=32,
						  epochs=20,
						  validation_split=split,
						  callbacks=[tensorboard])

				# Saving model to models folder
				model.save("models/{}".format(NAME))
				# Clearing session so the speed is not reduced as more models are trained
				tf.keras.backend.clear_session()

