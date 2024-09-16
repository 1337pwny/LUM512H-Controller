from PIL import Image, ImageOps
import numpy as np
import json
import os
dir="frames"
out = {
    "name": "pinki",
    "type": "image",
}
j=0
for filename in sorted(os.listdir(dir)):
    image = Image.open("./frames/"+filename)
    arr = np.array(image)
    int_arr = arr.astype(int)
    pixelmap = []
    frame={}
    for line in int_arr:
        newline = []
        # Converting to BW Array, white means of, any other color means on
        for elem in line:
            print(elem)
            if elem[0] < 255 and elem[1] < 255 and elem[2] < 255:
                newline.append(1)
            else:
                newline.append(0)
        pixelmap.append(newline)
    i=1
    for elem in pixelmap:
        frame[str(i)] = elem
        i=i+1
    out[str(j)] = frame
    j=j+1
print(out)
outJson=json.dumps(out)
f = open("./pinki.json", "w")
f.write(outJson)
f.close()