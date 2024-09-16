from PIL import Image, ImageOps
import numpy as np
import json

image = Image.open("./11.bmp")
arr = np.array(image)
int_arr=arr.astype(int)

pixelmap=[]
newline=""
for line in int_arr:
    #Converting to BW Array, white means of, any other color means on
    for elem in line:
        print(elem)
        if elem[0] < 255 and elem[1] < 255 and elem[2] < 255:
            newline=newline+str(1)
        else:
            newline=newline+str(0)
    newline=newline+";"
f = open("./11.dat", "w")
f.write(newline)
f.close()
