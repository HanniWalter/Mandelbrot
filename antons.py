import cmath
import random

from PIL import Image
import numpy as np
import seaborn as sns
from math import floor
import cv2
import sys

#globals
image_size = (400,400)
max_iteration = 500
frame = 0
max_frames = 10

coordinate = (-0.74364409961, 0.13182604688)#(-1.74364409961,-1+ 0.13182604688)
end_coordinate = (-0.74364409961, 0.13182604688)

zoom = 0.5
end_zoom = 10
palette = sns.cubehelix_palette(max_iteration, start=-.5, rot=0.8, light=0.7)

zoom_speed = 0.20

imageArr = None
ENUM_NO_CONTACT = 0
ENUM_CONTACT = 1
ENUM_ALL_CONTACT = 2
ENUM_BORDER = 3

def complex_from_tupel(t):
	return complex(t[0], t[1])
	pass

def complex_len(c):
	return cmath.sqrt((c.real * c.real + c.imag * c.imag)).real
	pass

def calc(c):
	z = c
	for i in range(1, max_iteration):
		z = z * z + c
		if (complex_len(z) > 2):
			return i
	return 0

def get_color_from_value(value):
	if value == 0:
		return [0, 0, 0]

	paletteColor = palette[int(value)]
	return [int(paletteColor[0] * 255), int(paletteColor[1] * 255), int(paletteColor[2] * 255)]

def get_coordinate_from_pixel(pixel):
	return (coordinate[0]+1/zoom*pixel[0]/image_size[0],
			coordinate[1]+1/zoom*pixel[1]/image_size[1])

def get_pixel_from_coordinate(coordinate):
	print("not implemented")
	return 0 

def findCenter(coord1, coord2):
	return coord1 + int((coord2 - coord1) / 2)

def colorArea(start, end, color):
	global imageArr
	if not np.array_equal(color, [255, 255, 0]):
		for x in range(start[0], end[0]):
			for y in range(start[1], end[1]):
				calculation = calc(complex_from_tupel(get_coordinate_from_pixel((x,y))))
				imageArr[x,y] = get_color_from_value(calculation)
	else:
		arr1 = np.arange(start[0], end[0])
		arr2 = np.arange(start[1], end[1])
		imageArr[start[0]:end[0],start[1]: end[1]] = [0,0,0]

def checkBorders(borders, start, end):
	if borders == [3,3,3,3]:
		return ENUM_CONTACT

	# border check here
	if borders == [0,0,0,0]:
		return ENUM_NO_CONTACT
	elif borders == [2,2,2,2]:
		return ENUM_ALL_CONTACT
	return ENUM_CONTACT

def getNextArea(start, end, depth=0):
	length = end[0] - start[0]

	# if depth >= 6:
	if length <= 3:
		colorArea(start, (end[0] + 1, end[1] + 1), [0,0,0])
		return

	borders = calcBorder(start, end)
	borderCheck = checkBorders(borders, start, end)

	if borderCheck == ENUM_CONTACT:
		xCenter = findCenter(start[0], end[0])
		yCenter = findCenter(start[1], end[1])

		newStart = (start[0] + 1, start[1] + 1)
		newEnd = (xCenter, yCenter)
		getNextArea(newStart, newEnd, depth + 1)

		newStart = (start[0] + 1, yCenter + 1)
		newEnd = (xCenter, end[1] - 1)
		getNextArea(newStart, newEnd, depth + 1)

		newStart = (xCenter + 1, start[1] + 1)
		newEnd = (end[0] - 1, yCenter)
		getNextArea(newStart, newEnd, depth + 1)

		newStart = (xCenter + 1, yCenter + 1)
		newEnd = (end[0] - 1, end[1] - 1)
		getNextArea(newStart, newEnd, depth + 1)
	elif borderCheck == ENUM_NO_CONTACT:
		pass
		colorArea((start[0] + 1, start[1] + 1), (end[0], end[1]), [0,0,255])
	elif borderCheck == ENUM_ALL_CONTACT:
		pass
		colorArea((start[0] + 1, start[1] + 1), (end[0], end[1]), [255,255,0])

def calcBorder(start=(0,0), end=(image_size[0]-1, image_size[1]-1)):
	global imageArr
	borders = [-1,-1,-1,-1]

	for i,b in enumerate(borders):
		contact = False
		onlyContact = True

		startLoc = (0,0)
		endLoc = (0,0)
		if i == 0:
			startLoc = start
			endLoc = (start[0], end[1])
		if i == 1:
			startLoc = (start[0] + 1, end[1])
			endLoc = (end[0] - 1, end[1])
		if i == 2:
			startLoc = (end[0], start[1])
			endLoc = end
		if i == 3:
			startLoc = (start[0] + 1, start[1])
			endLoc = (end[0] - 1, start[1])
		for x in range(startLoc[0], endLoc[0] + 1):
			for y in range(startLoc[1], endLoc[1] + 1):
				calculation = calc(complex_from_tupel(get_coordinate_from_pixel((x,y))))
				if x < image_size[0] and y < image_size[1]:
					if calculation > 0:
						imageArr[x,y] = get_color_from_value(calculation)
						onlyContact = False
					else:
						imageArr[x,y] = get_color_from_value(calculation)
						contact = True
		
		contactState = ENUM_NO_CONTACT
		if contact == True:
			contactState = ENUM_CONTACT
			if onlyContact == True:
				contactState = ENUM_ALL_CONTACT

		borders[i] = contactState

	return borders

def create_frame():
	global imageArr
	imageArr = np.empty((image_size[0], image_size[1], 3), dtype=np.uint8)
	getNextArea((0,0),(image_size[0], image_size[1]))

def make_video():
	zooming = True

	while zooming:
		global frame

		print("nextFrame")
		create_frame() 


		#save temp image for preview
		im = Image.fromarray((imageArr), 'RGB')
		im2 = Image.fromarray((cv2.resize(imageArr,(1000,1000))), 'RGB')
		im.save("temp.png")
		im2.save("temp2.png")

		#perform zoom
		global zoom
		zoom/=(1- zoom_speed)


		frame +=1
		#check end of loop
		zooming = not( zoom>end_zoom or (max_frames != 0 and max_frames<frame))

make_video()

