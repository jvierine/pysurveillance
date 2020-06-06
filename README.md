# pysurveillance

You can make a wifi enabled security camera with machine learning based object recognition with this piece of software.

Somebody stole my bike. I didn't find the security camera or software I wanted, so I tought I'd come up with something simple using OpenCV, Python, and Raspberry Pi. This is all hacked together in one evening, but it works on a Raspberry Pi 3 with about 20 fps. Only images with detected motion are fed into the deep neural network for object detection to save precious computing resources, which are somewhat limited on a Raspberry Pi.

Features:
- save jpg images when motion detected
- save h.264 codec mp4 files of movement detected each day
- creates a web with latest motion detection and the overview videos. 
- deep neural network based object detection to identify features in image

Future development ideas:
- Use detected features at certain times of day to raise an alarm e.g., with SMS or email.
