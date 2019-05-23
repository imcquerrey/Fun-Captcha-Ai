from selenium import webdriver
import time
import base64
from PIL import Image
import random
import pyautogui

# Open a firefox browser that can be automatically controlled by selenium
brow = webdriver.Firefox()

# Sends a get request to the login page of roblox and puts in random details then clicks login
brow.get('https://www.roblox.com/login')
brow.find_element_by_xpath('//*[@id="login-username"]').send_keys('test123')
brow.find_element_by_xpath('//*[@id="login-password"]').send_keys('test123')
brow.find_element_by_xpath('//*[@id="login-button"]').click()
tot = 0
pi = 0
while True:
	# Checks if the verify button is on screen meaning a fun captcha has appeared by using a picture of the button
	# to check and see if it is on the screen
	try:
		left, top, z, y = pyautogui.locateOnScreen('./lib/verify.png', grayscale=False, confidence=.5)
		# If it is located on the screen the left and top positions get 10 pixels add to them so the cursor can click on
		# the button
		left += 10
		top += 10
		pyautogui.click(left, top)
	except:
		# If the button is not located it will cause an error and the program will continue on
		pass

	# Checks if the circle of a fun captcha is on screen by using a picture of just the circle to check and see if it
	# is on the screen
	try:
		left, top, z, y = pyautogui.locateOnScreen('./lib/circle2.png', grayscale=False, confidence=.2)
		# If it is located on the screen then the selenium browser finds and switches to the iframe of the captcha
		# to access its contents then switches to the second iframe inside
		iframe = brow.find_element_by_xpath('//*[@id="fc-iframe-wrap"]')
		brow.switch_to.frame(iframe)
		iframe2 = brow.find_element_by_xpath('//*[@id="CaptchaFrame"]')
		brow.switch_to.frame(iframe2)
		# Locates an element with the id of "FunCAPTCHA" then executes a small script to grab the captcha image url
		# which is used to download the captcha image
		canvas = brow.find_element_by_id('FunCAPTCHA')
		canvas_base64 = brow.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
		canvas_png = base64.b64decode(canvas_base64)
		# A new png file is opened to save the captcha image
		with open("canvas.png", 'wb') as f:
			f.write(canvas_png)
		# The captcha image is then opened up and cropped so that only the circle with the image inside is part of the
		# new image which is then saved to a new image file
		img = Image.open('canvas.png')
		img = img.crop((110, 100, 260, 250))
		img.save('canvas2.png')
		# Rot variable is the degree of rotation that the program will use to make different rotated versions of the
		# original cropped image
		rot = 51.42857142857143
		for x in range(0,7):
			# The original cropped image is opened and converted to RGBA then rotated by the degree set in the rot
			# variable
			img = Image.open('canvas2.png').convert("RGBA")
			r = img.rotate(rot)
			# A new blank image is created to overlap the newly rotated image so there are no black gaps in the picture
			# and that the size stays the same
			fff = Image.new('RGBA', r.size, (255,) * 4)
			out = Image.composite(r, fff, r)
			a = out.convert(img.mode)
			# It is then saved to the Datacol folder where all images gathered all finally saved
			a.save('Datacol/%s.png' % pi)
			# Adding the same degree that rot was originally set to for the next iteration
			rot += 51.42857142857143
			# Adding 1 to pi which will be the new name of the next image saved
			pi += 1
		# Adding 1 to the tot counter which is used to know how many captchas were collected
		tot += 1
		print('Gathered: %s' % str(tot))
		# Sends a get request to the login page of roblox and puts in random details then clicks login to generate a
		# new captcha
		brow.get('https://www.roblox.com/login')
		brow.find_element_by_xpath('//*[@id="login-username"]').send_keys('test123')
		brow.find_element_by_xpath('//*[@id="login-password"]').send_keys('test123')
		brow.find_element_by_xpath('//*[@id="login-button"]').click()
	except:
		# If the circle of the captcha is not located it will cause an error and the program will continue on
		pass


	try:
		# Checks if the login page with the error saying invalid login details is on screen meaning a fun captcha did
		# not appear in which the program will click login again to try and get the site to generate a new captcha
		left, top, z, y = pyautogui.locateOnScreen('./lib/login.png', grayscale=False, confidence=.8)
		brow.find_element_by_xpath('//*[@id="login-button"]').click()
	except:
		# If the login page with the error saying invalid login details is not located it will cause an error and the program will continue on
		pass