from PIL import Image, ImageOps
import numpy as np
import json
image = Image.open("./splash.bmp")
arr = np.array(image)
int_arr=arr.astype(int)

pixelmap=[]
for line in int_arr:
    newline=[]
    #Converting to BW Array, white means of, any other color means on
    for elem in line:
        print(elem)
        if elem[0] < 255 and elem[1] < 255 and elem[2] < 255:
            newline.append(1)
        else:
            newline.append(0)
    pixelmap.append(newline)
out = {
    "name": "splash",
    "type": "image",
}
i=1
for elem in pixelmap:
    out[str(i)] = elem
    i=i+1
print(out)
outJson=json.dumps(out)
f = open("./splash.json", "w")
f.write(outJson)
f.close()