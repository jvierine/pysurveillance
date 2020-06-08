# import the necessary packages
import numpy as n
import argparse
import time
import cv2
import os
import glob
import pysurveillance_conf as conf

class yolo_detector:
    def __init__(self,yolo_dir="./yolo-coco"):
        self.yolo_dir=yolo_dir
        n.random.seed(42)
        self.labels = open("%s/coco.names"%(yolo_dir),"r").read().strip().split("\n")      
        self.colors = n.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")
        self.net = cv2.dnn.readNetFromDarknet("%s/yolov3.cfg"%(yolo_dir), "%s/yolov3.weights"%(yolo_dir))

    def detect(self,
               image,
               thresh_confidence=0.5,
               threshold=0.3):
        (H,W)=image.shape[:2]

        ln = self.net.getLayerNames()

        # determine only the *output* layer names that we need from YOLO
        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        
        blob = cv2.dnn.blobFromImage(image,
                                     1 / 255.0,
                                     (416, 416), # why 416?
                                     swapRB=True,
                                     crop=False)
        self.net.setInput(blob)
        start = time.time()
        layer_outputs = self.net.forward(ln)        
        end = time.time()

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []
        # loop over each of the layer outputs
        for output in layer_outputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = n.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > thresh_confidence:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * n.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        
        
        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes,
                                confidences,
                                thresh_confidence,
                                threshold)


        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                print(boxes[i])
                print(self.labels[classIDs[i]])
                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.colors[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.labels[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)
        
        # show the output image
        #cv2.imshow("Image", image)
        #cv2.waitKey(1)


yd=yolo_detector()

fl=glob.glob("vs/2*/*.jpg")
fl.sort()
for f in fl:
    image = cv2.imread(f)
    image=n.transpose(image,axes=[1,0,2])
    if conf.rotate:
        image=image[::-1,:,:].astype(n.uint8).copy()
    yd.detect(image)
