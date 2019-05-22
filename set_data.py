import numpy as np
import os
import cv2
import random
import pickle

# Configuring directory for where the training data is stored
DATADIR = 'C:\\Users\\IanW1\\PycharmProjects\\Like\\Like\\AI\\DATA3'
# Configuring the two possibilities for the ai to chose from. Data1 being that the image is not upright and Data2 being
# the image is upright. These are also the names of the two folders containing the training data
CATEGORIES = ['Data1', 'Data2']
# Setting image size which all data gathered is 150 pixels
IMG_SIZE = 150
training_data = []

def create_training_data():
	for category in CATEGORIES:
		# Getting data piece path
		path = os.path.join(DATADIR, category)
		# Getting what category the data piece is via the name of the folder it is located in
		class_num = CATEGORIES.index(category)
		for img in os.listdir(path):
			# Try and Except statement in case one of the data pieces is invalid
			try:
				# Setting image size which all data gathered is 150 pixels
				img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
				# Resizing the image array to the set size of 150 pixels in case one of the data pieces happens to
				# have a different size
				new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
				# Appending the new array to the training data list along with what category it is
				training_data.append([new_array, class_num])
			except:
				pass


def trainingsave():
	# Converting images to gray scale then to arrays and appending them to the training_data list
	create_training_data()
	print(len(training_data))
	# Shuffling the positioning of each data piece in the list
	random.shuffle(training_data)

	X = []
	Y = []

	# Seperating the image array from the category into X, Y
	for features, label in training_data:
		X.append(features)
		Y.append(label)


	# Converting all image arrays in the list X to numpy arrays
	X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)


	# Storing the values of the X, Y lists through pickle
	pickle_out = open("X.pickle", "wb")
	pickle.dump(X, pickle_out)
	pickle_out.close()

	pickle_out = open("Y.pickle", "wb")
	pickle.dump(Y, pickle_out)
	pickle_out.close()


trainingsave()


