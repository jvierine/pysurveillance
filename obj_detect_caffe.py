# import the necessary packages
import numpy as n
import argparse
import time
import cv2
import os
import glob

class yolo_detector:
    def __init__(self,
                 caffe_proto_txt="MobileNetSSD_deploy.prototxt.txt",
                 caffe_model_file="MobileNetSSD_deploy.caffemodel",
                 ):
        n.random.seed(42)
        self.classes = ["background", "aeroplane", "bicycle", "bird", "boat",
	                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	                "sofa", "train", "tvmonitor"]

        self.colors = n.random.uniform(0, 255, size=(len(self.classes), 3))
#        self.colors = n.random.randint(0, 255, size=(len(self.classes), 3), dtype="uint8")        
        self.net = cv2.dnn.readNetFromCaffe(caffe_proto_txt, caffe_model_file)
        

    def detect(self,
               image,
               thresh_confidence=0.5,
               threshold=0.3):
        
        (H,W)=image.shape[:2]
        
        blob = cv2.dnn.blobFromImage(image,
                                     0.007843,
                                     (300, 300),
                                     127.5)
        # set the blob as input to our deep learning object
        # detector and obtain the detections
        self.net.setInput(blob)
        detections = self.net.forward()
        print(detections)
        if detections is not None:
            # loop over the detections
            for i in n.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                print(confidence)
                if confidence < thresh_confidence:
                    continue
                # otherwise, extract the index of the class label from
                # the `detections`, then compute the (x, y)-coordinates
                # of the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                print(idx)
                dims = n.array([W, H, W, H])
                box = detections[0, 0, i, 3:7] * dims
                (startX, startY, endX, endY) = box.astype("int")
                
                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(self.classes[idx],
                                             confidence * 100)
                print(self.colors[idx])
                print(idx)
                cv2.rectangle(image, (startX, startY), (endX, endY), self.colors[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
			    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            self.colors[idx], 2)
        # show the output frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF


                



yd=yolo_detector()

fl=glob.glob("vs/2*/*.jpg")
fl.sort()
for f in fl:
    image = cv2.imread(f)
    image=n.transpose(image,axes=[1,0,2])
    image=image[::-1,:,:].astype(n.uint8).copy()
#    print(image.dtype)
    yd.detect(image)
