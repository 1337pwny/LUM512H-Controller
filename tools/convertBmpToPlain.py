from PIL import Image, ImageOps
import numpy as np
import json

from tools.convertBmpToJsonArray import newline

image = Image.open("./01.bmp")
arr = np.array(image)
int_arr=arr.astype(int)

pixelmap=[]
for line in int_arr:
    newline="data#"
    #Converting to BW Array, white means of, any other color means on
    for elem in line:
        print(elem)
        if elem[0] < 255 and elem[1] < 255 and elem[2] < 255:
            newline=newline+str(1)
        else:
            newline=newline+str(0)
    pixelmap.append(newline)
f = open("./01.dat", "w")

for elem in pixelmap:
    print(elem)
    f.write(elem+"\n")
f.close()
