import cv2
import numpy as n
import glob
import os

max_n=600
fl=glob.glob("vs/test*.jpg")
fl.sort()
# only max_n latest images
if len(fl) > max_n:
    fl=fl[(len(fl)-max_n):len(fl)]

# what is the image size
for filename in fl[0:1]:
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)

# this doesn't work
#out = cv2.VideoWriter('vs/latest_tmp.mp4',cv2.cv.CV_FOURCC(*"X264"),5.0, size)
# this magic code/contained combo seems to work. 
out = cv2.VideoWriter('vs/latest_tmp.avi',cv2.cv.CV_FOURCC(*"MJPG"),5.0, size)

# open files one at a time to avoid excessive ram use
for filename in fl:
    print(filename)
    img = cv2.imread(filename)
    out.write(img)
out.release()

# copy tmp file to one on web page
os.system("cp vs/latest_tmp.avi vs/latest.avi")
# convert to mp4 for html embedding
os.system("avconv -y -i vs/latest.avi -c:v libx264 vs/latest_tmp.mp4")
# copy tmp file to file on web page
os.system("cp vs/latest_tmp.mp4 vs/latest.mp4")
