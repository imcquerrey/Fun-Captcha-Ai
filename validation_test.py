from PIL import Image
import cv2
import tensorflow as tf
import glob
import os
from shutil import copyfile
import random

# Configuring the two possibilities for the ai to chose from. Data1 being that the image is not upright and Data2 being
# the image is upright. These are also the names of the two folders containing the training data
CATEGORIES = ["Data1", "Data2"]
# Getting all models to test from the test folder
models = glob.glob('./models3/*')

def prepare(filepath):
	# Setting image size which all data gathered is 150 pixels
	IMG_SIZE = 150
	# Setting image size which all data gathered is 150 pixels
	img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
	# Resizing the image array to the set size of 150 pixels in case one of the data pieces happens to
	# have a different size
	new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
	# Returning the new array for the ai to check
	return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
#, '1.png', '2.png', '3.png', '4.png'
# Adding all picture file names to the list that the ai will be tested against
pacs = ['0.png', '1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png']

# Setting up counters for each of the different models that will be tested
total = {}
for mod in models:
	total[mod] = 0

# Clearing the previous images the ai chose
for fol in range(1,9):
	folpics = glob.glob('./pi/%s/*' % fol)
	for fl in folpics:
		os.remove(fl)

pp = []
for pic in pacs:
	# Copying the image that will be used for testing into a temporary place
	copyfile(pic, 'pi/0.png')
	pp.append('----------------------------------------')
	modelpos = 0
	for mod in models:
		modelpos += 1

		# Loading the model that will be used for testing
		model = tf.keras.models.load_model(mod)
		# Making the prediction on the newly copied image
		prediction = model.predict([prepare(pic)])
		good = ''
		# Checking the prediction was predicted as upright (Data2)
		if CATEGORIES[int(prediction[0][0])] == 'Data2':
			# Adding True to the good variable which will be checked after all possible image rotations have been checked
			good = good + 'True'
			# Saving the name of the image which the first one is always named 0
			savepic = '0'

		# Number to rotate image by
		a3 = 51.42857142857143
		# Iterating 6 times to get every possible rotation of the image
		for x in range(1,7):
			# Converting the origonal image to RGBA format then rotating it by the set degree (a3)
			img = Image.open(pic).convert("RGBA")
			r = img.rotate(a3)
			# A new blank image is then created to be used to overlap the newly rotated image to avoid black spacing
			# and making sure the image size stays the same
			fff = Image.new('RGBA', r.size, (255,)*4)
			out = Image.composite(r, fff, r)
			a = out.convert(img.mode)
			# The newly rotated image is then saved to the temp folder along with other rotated images of its kind and
			# the origonal image
			a.save('pi/%s.png' % x)

			# Making the prediction on the newly rotated image
			prediction = model.predict([prepare('pi/%s.png' % x)])

			# Checking the prediction was predicted as upright (Data2)
			if CATEGORIES[int(prediction[0][0])] == 'Data2':
				# Adding True to the good variable which will be checked after all possible image rotations have been checked
				good = good + 'True'
				# Saving the name of the image which the first one is always named 0
				savepic = '0'

			# Adding the same degree that a3 was originally set to for the next iteration
			a3 += 51.42857142857143

		# After all possible varations of the origonal image have been tested the good variable is then tested to see
		# if the ai only predicted that one of the seven images was correctly rotated which no matter the origonal image
		# there will only be one correctly rotated image
		if good == 'True':
			# Append to the console list the image and model used and saying that the ai predicted correctly
			pp.append('Pic: %s | Valid | %s' % (pic, mod))
			# Adding one to the current model in use counter
			orig = int(total[mod]) + 1
			total[mod] = orig

			# Gettng a random value to use for the image name
			i = random.randint(0,100)
			# Copying the correctly rotated image to the folder of the model in use
			copyfile('pi/%s.png' % savepic, 'pi/%s/%s.png' % (str(modelpos), str(int(savepic)+i)))

		# If good is not equal to True that can mean that the ai guess more than one image was correctly rotated which
		# would always be incorrect or it never predicted one of the images was correctly rotated
		else:
			# Append to the console list the image and model used and saying that the ai predicted incorrecttly
			pp.append('Pic: %s | Invalid | %s' % (pic, mod))

		# Clearing session so the speed is not reduced as more models are trained
		tf.keras.backend.clear_session()

# Adding the counters of the models to the console list
pp.append(total)

# Printing out the entire console
for x in pp:
	print(x)

# After all models have been tested you should check each model folder that contained the predictions of the model
# to check that the predictions are 100% correct