import cv2
import numpy as n
import glob

img_array = []
max_n=100
fl=glob.glob("vs/test*.jpg")
fl.sort()
if len(fl) > max_n:
    fl=fl[(len(fl)-max_n):len(fl)]
    
for filename in fl:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    print(filename)

out = cv2.VideoWriter('vs/latest.avi',cv2.cv.CV_FOURCC(*"MJPG"),5.0, size)

for i in range(len(img_array)):
    print(i)
    out.write(img_array[i])
out.release()
