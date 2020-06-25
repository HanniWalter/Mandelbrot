import cmath
import random
import math
from PIL import Image
import numpy as np
import numpy 
import seaborn as sns
from math import floor
import cv2
import time
from numba import jit
import numpy as np
import time
from numba import njit, prange
from numba.typed import List

#globals

image_size = (200,200)
max_iteration = 800
frame = 0
max_frames = 1000
FPS = 60

coordinate = (-0.74364409961, 0.13182604688)#(-1.74364409961,-1+ 0.13182604688)
end_coordinate = (-0.74364409961, 0.13182604688)

zoom = 0.5
end_zoom = 1000000
#palette = sns.cubehelix_palette(max_iteration / stepReduce, start=-.5, rot=2, light=0.7)
palette = sns.cubehelix_palette(max_iteration, start=-.5, rot=0.8, light=0.7)
#palette = sns.cubehelix_palette(max_iteration, start=.4, rot=2.5, light=0.7, gamma=1.6)

#x = np.arange(image_size[0]*image_size[1])

@jit(nopython=True)
def scalejit(x):
	return complex((floor(x/image_size[0])/image_size[0]*2 -1) , ((x%image_size[1])/image_size[1]*2 -1))

def scale (x):
	#print (complex((floor(x/image_size[0])/image_size[0]*2 -1) , ((x%image_size[1])/image_size[1]*2 -1)))
	#print(calc(complex((floor(x/image_size[0])/image_size[0]*2 -1) , ((x%image_size[1])/image_size[1]*2 -1))))
	return complex((floor(x/image_size[0])/image_size[0]*2 -1) , ((x%image_size[1])/image_size[1]*2 -1))

@jit(nopython=True)
def complex_lenjit(c):
    return cmath.sqrt((c.real * c.real + c.imag * c.imag)).real


def complex_len(c):
    return cmath.sqrt((c.real * c.real + c.imag * c.imag)).real

@jit(nopython=True)
def calcjit(c):
    z = c
    for i in range(1, max_iteration):
        z = z * z + c
        if (complex_lenjit(z) > 2):
            return i
    return 0
    
def calc(c):
    z = c
    for i in range(1, max_iteration):
        z = z * z + c
        if (complex_len(z) > 2):
            return i
    return 0


@njit(parallel=True)
def loopp(pc):
	#picraw = np.empty((image_size[0]*image_size[1]),dtype=np.uint16)
	pic = np.empty((image_size[0]*image_size[1],3),dtype=np.uint8)
	x = prange(image_size[0]*image_size[1])
	for i in x:
		calc = calcjit(scalejit(i))
		if calc == 0:
			pic[i] = [0, 0, 0]
		else:
			pic[i] = pc[calc]	
	return pic.reshape((image_size[0],image_size[1],3))


def loop():
	pic = np.empty((image_size[0]*image_size[1],3),dtype=np.uint8)
	x = np.arange(image_size[0]*image_size[1])


	for i in x:
		value = calc(scale(i))

		if value == 0:
			pic[i] = [0, 0, 0]
		else:
			pic[i] = pc[calc]	
	return pic.reshape((image_size[0],image_size[1],3))

@jit(nopython=True)
def loopjit(pc):
	#picraw = np.empty((image_size[0]*image_size[1]),dtype=np.uint16)
	pic = np.empty((image_size[0]*image_size[1],3),dtype=np.uint8)
	x = np.arange(image_size[0]*image_size[1])
	for i in x:
		calc = calcjit(scalejit(i))
		if calc == 0:
			pic[i] = [0, 0, 0]
		else:
			pic[i] = 	pc[calc]
	return pic.reshape((image_size[0],image_size[1],3))



pc = np.empty([max_iteration,3],dtype=np.uint8)
for i in range(int(max_iteration)):
	paletteColor = palette[i]
	pc[i] = [int(paletteColor[0] * 255), int(paletteColor[1] * 255), int(paletteColor[2] * 255)]

print(1/60)

#start = time.time()
#im = Image.fromarray(loop())
#im.save("1.png")
#end = time.time()
#print("Elapsed (no compilation) = %s" % (end - start))

start = time.time()
im = Image.fromarray(loopjit(pc))
im.save("2.png")
end = time.time()
print("Elapsed (with compilation) = %s" % (end - start))

start = time.time()
im = Image.fromarray(loopjit(pc))
im.save("3.png")
end = time.time()
print("Elapsed (with compilation 2) = %s" % (end - start))


###paralel

start = time.time()
im = Image.fromarray(loopp(pc))
im.save("4.png")
end = time.time()
print("Elapsed (with compilation parallel) = %s" % (end - start))

start = time.time()
im = Image.fromarray(loopp(pc))
im.save("5.png")
end = time.time()
print("Elapsed (with compilation parallel 2) = %s" % (end - start))

start = time.time()
im = Image.fromarray(loopp(pc))
im.save("6.png")
end = time.time()
print("Elapsed (with compilation parallel 3) = %s" % (end - start))