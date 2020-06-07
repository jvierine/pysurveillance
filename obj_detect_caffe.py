#
# requires opencv 3.3+
#
import numpy as n
import argparse
import time
import cv2
import os
import glob
import re

import date_print_util as dpu
import pysurveillance_conf as conf
if conf.send_alerts:
    import alert_phone

class caffe_detector:
    def __init__(self,
                 caffe_proto_txt="caffe/MobileNetSSD_deploy.prototxt.txt",
                 caffe_model_file="caffe/MobileNetSSD_deploy.caffemodel",
                 reported_classes=["person"]): # only report these
        
        n.random.seed(42)
        self.classes = ["background", "aeroplane", "bicycle", "bird", "boat",
	                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	                "sofa", "train", "tvmonitor"]
        
        self.reported_classes=reported_classes
        self.colors = n.random.uniform(0, 255, size=(len(self.classes), 4))
        self.colors[:,3]=64
        self.net = cv2.dnn.readNetFromCaffe(caffe_proto_txt, caffe_model_file)
        

    def detect(self,
               image,
               output_image_fname="label.jpg",
               label_fname="label.txt",
               thresh_confidence=0.3,
               threshold=0.3):

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), conf.image_quality]
        
        (H,W)=image.shape[:2]

        blob = cv2.dnn.blobFromImage(image,
                                     0.007843,
                                     (300, 300),
                                     127.5)
        
        # set the blob as input to our deep learning object
        # detector and obtain the detections
        self.net.setInput(blob)
        detections = self.net.forward()

        parsed_detections=[]
        if detections is not None:
            # loop over the detections
            for i in n.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence < thresh_confidence:
                    continue
                
                idx = int(detections[0, 0, i, 1])

                dims = n.array([W, H, W, H])
                box = detections[0, 0, i, 3:7] * dims
                (startX, startY, endX, endY) = box.astype("int")

                
                parsed_detections.append({"class":self.classes[idx],"box":[startX,startY,endX,endY],"confidence":confidence})
                print("detected %s with %1.2f probability"%(self.classes[idx],confidence*100.0))
                
                if self.classes[idx] in self.reported_classes:
                    if conf.send_alerts:
                        alert_phone.send_alert()
                    # otherwise, extract the index of the class label from
                    # the `detections`, then compute the (x, y)-coordinates
                    # of the bounding box for the object
                    
                    # draw the prediction on the frame
                    label = "{}: {:.2f}%".format(self.classes[idx],
                                                 confidence * 100)
                    cv2.rectangle(image, (startX, startY), (endX, endY), self.colors[idx], 2)


                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                self.colors[idx], 2)
                    # only make label image if there is a detected label
                    cv2.imwrite(output_image_fname,image,encode_param)

                    

        fo=open(label_fname,"w")
        for p in parsed_detections:
            fo.write("%s %1.3f %d %d %d %d\n"%(p["class"],p["confidence"],p["box"][0],p["box"][1],p["box"][2],p["box"][3]))
        fo.close()
                



cd=caffe_detector()

fl=glob.glob("vs/2*/det-*.jpg")
fl.sort()
fl=fl[::-1]
for f in fl:
    if os.path.exists("%s.label"%(f)):
        print("already exists")
    else:
        print("labeling %s"%(f))
        image = cv2.imread(f)
        if conf.rotate_on_detection:
            image=n.transpose(image,axes=[1,0,2])
            image=image[::-1,:,:].astype(n.uint8).copy()

        prefix=re.search("(.*)/det-.*.jpg",f).group(1)
        postfix=re.search(".*/det(-.*).jpg",f).group(1)
        t_event=float(re.search(".*/det-(.*).jpg",f).group(1))
        
        image_fname="%s/label%s.jpg"%(prefix,postfix)
        label_fname="%s.label"%(f)
        print("writing image %s labels to %s time %s"%(image_fname,label_fname,dpu.unix2datestr(t_event)))
            
        cd.detect(image=image,
                  label_fname=label_fname,
                  output_image_fname=image_fname)
        # done for now
        exit(0)
