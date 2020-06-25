import cmath
import random

from PIL import Image
import numpy as np
import seaborn as sns
from math import floor
import cv2

ModX = 0
ModY = 0
frame = 0
frames = 3
FPS = 5
image_size = (70,70)
#start_pic = ((-2.5, -2), (1.5, 2))
start_zoom = 2
end_zoom = 0.0000001
start = (-0.74364409961, 0.13182604688)
end = (-0.74364409961, 0.13182604688)
zoom_speed = 0.1
#start_bountries = ((-1.8, -1.2), (0.6, 1.2))
#end_bountries = ((-1, -0.5), (-0.5, 0))
max_iteration = 100

#palette = sns.cubehelix_palette(max_iteration / stepReduce, start=-.5, rot=2, light=0.7)
palette = sns.cubehelix_palette(max_iteration, start=-.5, rot=0.8, light=0.7)
#palette = sns.cubehelix_palette(max_iteration, start=.4, rot=2.5, light=0.7, gamma=1.6)


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


def complex_len(c):
    return cmath.sqrt((c.real * c.real + c.imag * c.imag)).real


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


def get_point_from_pixel(zoom, pixel, offset):
    upper, left = 
    down, rigth = boundries[1]
    return (upper + (down - upper) * pixel[0] / image_size[0], left + (rigth - left) * pixel[1] / image_size[1])

def get_pixel_from_point(point,pixel,offset):


def create_frame(boundries):
    returner = np.zeros((image_size[0], image_size[1], 3), dtype=np.uint8)

    for x in range(image_size[0]):
        #printStatus("Calculating Image", 1000, int(int((x / (image_size[0])) * 10000) / 10))
        print("frame ",frame,"/",frames,"       ",x,"/",image_size[0])
        for y in range(image_size[1]):
            calculation = calc(complex_from_tupel(get_point_from_pixel(boundries, (x, y))))
            returner[x, y] = get_color_from_value(calculation)
    return returner

def scale_up_image(raw,old_boundries,new_boundries):
    returner0 = np.zeros((image_size[0],len(raw[0]), 3), dtype=np.uint8)
    number_of_new_coloums = image_size[0] - len(raw[0])
    print("new coloums: ",number_of_new_coloums)
    if not number_of_new_coloums==0:
        every_colum_a_new_coloum = int(image_size[0]/number_of_new_coloums)
        boundies_temp = ((old_boundries[0][0],new_boundries[0][1]),(old_boundries[1][0],new_boundries[1][1]))
        readX = 0
        ModX = random.randrange(0, every_colum_a_new_coloum)
        for x in range(image_size[0]):
            if x % every_colum_a_new_coloum == ModX or readX>=len(raw):
                for y in range(len(raw[0])):
                    calculation = calc(complex_from_tupel(get_point_from_pixel(boundies_temp, (x, y))))
                    returner0[x, y] = get_color_from_value(calculation)
            else:
                returner0[x]= raw[readX]
                readX +=1
        #for y in range(image_size[0]):
        #   returner = raw[x,y]
    else:
        returner0 = raw
    returner1 = np.zeros((image_size[0],image_size[1], 3), dtype=np.uint8)
    number_of_new_rows = image_size[1] - len(raw[1])
    if not number_of_new_rows == 0:
        every_rows_a_new_row = int(image_size[1]/number_of_new_rows)
        readY = 0
        ModY = random.randrange(0,every_rows_a_new_row)
        for y in range(image_size[1]):
            if y % every_rows_a_new_row == ModY or readY >=len(returner0[0]):
                for x in range(image_size[0]):
                    calculation = calc(complex_from_tupel(get_point_from_pixel(new_boundries, (x, y))))
                    returner1[x, y] = get_color_from_value(calculation)
            else:
                returner1[:,y] = returner0[:,readY]
                readY +=1
    else:
        returner1 = returner0
    return returner1



def scale_up_image_new(raw,a,new_boundries):
    image = cv2.resize(raw,image_size)
    for x in range(len(image)):
        print("frame ", frame, "/", frames, "       ", x, "/", image_size[0])
        for y in range(int(len(image[0])/2)):
            calculation = calc(complex_from_tupel(get_point_from_pixel(new_boundries, (x, y))))
            image[x, y] = get_color_from_value(calculation)

    return image


def get_bountries(center,zoom):
    return ((center[0]-zoom/2,
             center[1]-zoom/2),
            (center[0]+zoom/2,
             center[1]+zoom/2))

def make_vid():
    out = cv2.VideoWriter('project3.avi', cv2.VideoWriter_fourcc(*'DIVX'), FPS, image_size)
    zooming = True
    center0 = start
    zoom = start_zoom
    bountries0 = get_bountries(center0, zoom)
    image0 = create_frame(bountries0)
    out.write(image0)
    zoommodifier= 1 - (zoom_speed/2)
    #end_bountries = get_bountries(end, end_zoom)
    while(zooming):
        im = Image.fromarray((image0), 'RGB')
        im.save("newPic5.png")
        global frame
        frame += 1
        center1 = (center0[0]+zoommodifier*(end[0]-center0[0]),(center0[1]+zoommodifier*(end[1]-center0[1])))
        bountries1 = get_bountries(center1, zoom)
        print("im0 ",image0.shape)
        pixel_bountries_with_old_center = ((0.5*image_size[0]-zoom*image_size[0],0.5*image_size[1]-zoom*image_size[1]),(0.5*image_size[0]+zoom*image_size[0],0.5*image_size[1]+zoom*image_size[1]))
        #
        old_length = bountries0[1][0]-bountries0[0][0]
        old_width = bountries0[1][1]-bountries0[0][1]
        #left
        left = int(pixel_bountries_with_old_center[0][0]+image_size[0]*(center1[0]-center0[0])*old_length)
        #top
        top = int(pixel_bountries_with_old_center[0][1]+image_size[1]*(center1[1]-center0[1])*old_width)
        #right
        right = int(pixel_bountries_with_old_center[1][0]+image_size[0]*(center1[0]-center0[0])*old_length)
        #bottom
        bottom = int(pixel_bountries_with_old_center[1][1]+image_size[1]*(center1[1]-center0[1])*old_length)
        image1 = image0[left:right,top:bottom].copy() 
        #for x in range(int(image_size[0]*(bountries1[0][0]-bountries0[0][0])/(bountries0[1][0]-bountries0[0][0])),
        #               int(image_size[0]*(bountries1[1][0]-bountries0[0][0])/(bountries0[1][0]-bountries0[0][0]))):
        #    for y in range(int(image_size[1]*(bountries1[0][1]-bountries0[0][1])/(bountries0[1][1]-bountries0[0][1])),
        #                   int(image_size[1]*(bountries1[1][1]-bountries0[0][1])/(bountries0[1][1]-bountries0[0][1]))):
        #        print(x,y)
        #        image1[x,y]=image0[x,y]
        print("im1 ",image1.shape)
        #image2
        image2 = scale_up_image_new(image1,bountries0,bountries1)
        #image2 = cv2.resize(image1,image_size)
        out.write(image2)
        image0 = image2


        bountries0 = bountries1
        center0 = center1
        #image0 = create_frame(bountries)



        #print(frame)
        if frame >= frames:
            zooming = False
        if zoom < end_zoom:
            zooming = False

        zoom *= zoommodifier

        center = center1

    out.release()
    print("ready")

def make_pic(s):
    if s == "start":
        im = Image.fromarray(create_frame(get_bountries(start,start_zoom)), 'RGB')
    elif s == "end":
        im = Image.fromarray(create_frame(get_bountries(end,end_zoom)), 'RGB')
    im.save("newPic4.png")
    print("ready")

#("end")
make_vid()
#make_pic("end")