# pysurveillance

Somebody stole my bike. I didn't find the security camera or software I wanted, so I tought I'd come up with something simple using opencv, python, and raspberry pi. This is all hacked together in one evening, but it works on a raspberry pi 3 with about 20 fps. 

Features:
- save jpg images when motion detected
- save h.264 codec mp4 files of movement detected each day
- creates a web with latest motion detection and the overview videos. 
- Deep neural network based object detection to identify features in image

Future development ideas:
- Use detected features at certain times of day to raise an alarm e.g., with SMS or email.
