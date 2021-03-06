# pysurveillance
![Example](https://github.com/jvierine/pysurveillance/blob/master/example/label-1591336913.66.jpg)

You can make a wifi enabled security camera with machine learning based object recognition with this piece of software, which can call your phone and alert you if it detects a predefined object in the camera (e.g., person in the middle of the night).

Somebody stole my bike. I didn't find the security camera or software I wanted, so I tought I'd come up with something simple using OpenCV, Python, and Raspberry Pi. This is all hacked together in one evening, but it works on a Raspberry Pi 3 with about 20 fps. Only images with detected motion are fed into the deep neural network for object detection to save precious computing resources, which are somewhat limited on a Raspberry Pi.

Features:
- save jpg images when motion detected
- deep neural network based object detection to identify features in image
- save h.264 codec mp4 files of objects of interest detected each day
- creates a web page with latest motion detection and the overview videos. 
- use detected features at certain times of day to raise an alarm e.g., with SMS or email.

I found this tutorial very helpful when making this software:
https://www.pyimagesearch.com/2017/10/16/raspberry-pi-deep-learning-object-detection-with-opencv/
