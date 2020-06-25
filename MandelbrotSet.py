import cmath
import random
import math
from PIL import Image
import numpy as np
import seaborn as sns
from math import floor
import cv2
import time

#globals
image_size = (800,800)
max_iteration = 800
frame = 0
max_frames = 1000
FPS = 60

coordinate = (-0.74364409961, 0.13182604688)#(-1.74364409961,-1+ 0.13182604688)
end_coordinate = (-0.74364409961, 0.13182604688)

zoom = 0.5
end_zoom = 1000000
palette = sns.cubehelix_palette(max_iteration, start=-.5, rot=0.8, light=0.7)

zoom_speed = 0.050

def printStatus(message, maxC, curC):
    if curC > maxC:
        return
    if curC % (maxC / 10000) > 1 and maxC != curC:
        return
    count = floor(20 * (curC / maxC))
    smallCount = int(200 * (curC / maxC)) % 10
    print(message + "   [" + "#" * count + " " * (20 - count) + "]   " + ">" * smallCount + " " * (
                10 - smallCount) + "   (" + str(curC) + "/" + str(maxC) + ")", end="\r")
    if maxC == curC:
        print(message + "   [" + "#" * 20 + "]   DONE")

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

def create_slow_pixel(x,y):
	calculation = calc(complex_from_tupel(get_coordinate_from_pixel((x,y))))
	return  get_color_from_value(calculation)


def create_fast_pixel(x,y,raw):
	if x == 0 or y == 0 or x == image_size[0] or y == image_size[1]:
		return create_slow_pixel(x,y)
	sli = raw[x-1:x+1,y-1,y+1].copy()
	sli[1,1] = (0,0,0)
	if(raw[x-1,y-1] == (0,0,0) or raw[x+1,y-1] == (0,0,0) or raw[x-1,y+1] == (0,0,0) or raw[x+1,y+1] == (0,0,0)):
		return(0,0,0)
	return create_slow_pixel(x,y)

def resize(raw):
	x0 = raw.shape[0]
	y0 = raw.shape[1]
	x1 = image_size[0]
	y1 = image_size[1]
	returner = np.empty((x1,y1,3), dtype=np.uint8)
	new_xs = x1-x0
	#new_ys_size = y1-y0
	x_offset = random.randrange(math.floor(x0/new_xs))
	new_ys = y1-y0
	#new_ys_size = y1-y0
	y_offset = random.randrange(math.floor(y0/new_ys))
	used_x = 0

	for x in range(x1):
		print("frame ",frame,"/",max_frames,"       ",x,"/",image_size[0])
		if x%math.floor(x0/new_xs)==x_offset:
			for y in range(y1):
				create_slow_pixel(x,y)
				#if y%math.floor(y0/new_ys)==y_offset:
				#	print(x,y)
				#	returner[x,y] = raw[used_x,used_y]#new
				#else:
				#	returner[x,y]= raw[used_x,used_y]
				#	used_y +=1
		else:
			

			used_y = 0

			for y in range(y1):
				if y%math.floor(y0/new_ys)==y_offset:
					create_slow_pixel(x,y)
				else:
					returner[x,y]= raw[used_x,used_y]
					used_y +=1
			used_x +=1		
	return returner

def create_frame(old_frame):
	if old_frame.size == 0:
		returner = np.empty((image_size[0], image_size[1], 3), dtype=np.uint8)
		for x in range(image_size[0]):
			print("frame ",frame,"/",max_frames,"       ",x,"/",image_size[0])
			for y in range(image_size[1]):
				returner[x, y] = create_slow_pixel(x,y)
	else:
		returner = resize(old_frame)
		#for x in range(int(image_size[0]/2)):
			#print("frame ",frame,"/",max_frames,"       ",x,"/",int(image_size[0]))
			
			#coef = 1
			#r = random.sample(range(image_size[1]),int((image_size[1])*zoom_speed/coef))
			#for y in r:
			#		calculation = calc(complex_from_tupel(get_coordinate_from_pixel((x,y))))
			#		returner[x, y] = get_color_from_value(calculation)
	return returner

def make_video():
	out = cv2.VideoWriter('project4.avi', cv2.VideoWriter_fourcc(*'DIVX'), FPS, image_size)
	old_image = np.empty((0,0))
	zooming = True
	im = None
	while zooming:
		global zoom

		#print(zoom)
		new_image = create_frame(old_image) 
		#save temp image for preview
		im = Image.fromarray((new_image), 'RGB')
		im2 = Image.fromarray((cv2.resize(new_image,(1000,1000))), 'RGB')
		im.save("temp.png")
		im2.save("temp2.png")

		out.write(new_image)

		#create scaled down version of the old pic
		old_image = new_image[:int(image_size[0]*(1-zoom_speed)),:int(image_size[1]*(1-zoom_speed))]


		#perform zoom
		zoom/=(1- zoom_speed)

		global frame
		frame +=1
		#check end of loop
		zooming = not( zoom>end_zoom or (max_frames != 0 and max_frames<frame))
	im.save("end_temp.png")
	out.release()
	
def make_image():
	global zoom
	zoom = end_zoom
	global coordinate
	coordinate = end_coordinate
	im = Image.fromarray((create_frame(np.empty((0,0))) ), 'RGB')
	im.save("end_image.png")

make_video() 