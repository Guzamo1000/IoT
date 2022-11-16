import cv2
import numpy as np
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import time

import cv2
import numpy as np
from cv2 import dnn
from numpy.lib.type_check import imag
from post_data import camera_run

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.python.framework.ops import device
import tensorflow as tf
# from post import up_data
import base64
from datetime import datetime
import urllib.request


class ObjectDetection:

    def __init__(self):
        self.model = "D:\PTIT\IoT\d\project\detect\MobileNetSSD_deploy.caffemodel"
        self.prototxt = "D:\PTIT\IoT\d\project\detect\MobileNetSSD_deploy.prototxt"
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        # self.url=url
    def define_classes(self):
        """Define classes and associates colors randomly"""

        self.classes = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def run_detection(self):
        model=tf.keras.models.load_model(r'D:\PTIT\IoT\d\project\detect\model_mobinetv2_35_epoch.h5') # model h5

        print("Start object detection ...")

        self.define_classes()
        vs = WebcamVideoStream(0).start()
        fps = FPS().start()
        # L=[]
        while True:

            frame = vs.read()
            # img=urllib.request.urlopen(self.url)
            # img_np= np.array(bytearray(img.read()),dtype=np.uint8)
            # frame=cv2.imdecode(img_np,-1)
            (h, w) = frame.shape[:-1]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                         scalefactor=0.007843, size=(300, 300), mean=127.5)
            self.net.setInput(blob)
            detections = self.net.forward()

            # Loop over detected objects
            for i in np.arange(0, detections.shape[2]):

                # Get proba for each object
                probability = detections[0, 0, i, 2]

                # Set up threshold for filtering detection
                if probability > 0.5:
                    # Get prediction index
                    index = int(detections[0, 0, i, 1])

                    # Get bounding box coordinates
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    print(box)#(x,y,w,h)
                    #(startX, startY, endX, endY) = box.astype("int")
                    (x,y,w,h) = box.astype("int")

                    cv2.rectangle(frame, (x+10,y+5), (w+10,h+5), (255,0,0), 2)
                    face=frame[y+5:h+5, x+15:w+10]

                    face = cv2.resize(face,(256,256))
                    face2 = img_to_array(face)
                    face2 = np.expand_dims(face2,axis=0)
                    
                    # faces.append(face2)
                    label=None
                    pred = model.predict(face2)
                    idx_max = np.argmax(pred[0])
                    
                    class_names = ['cardboard','glass','metal','paper','plastic','trash']
                    cv2.putText(frame, class_names[idx_max], (x+5, y-15),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                    label=class_names[idx_max]
                    # L.append(label)
                    print(label)
                    # print(f"face {face}")
                    
                    
                    '''
                    label = "{}: {:.2f}%".format(self.classes[index], probability * 100)

                    y = startY - 10 if startY - 10 > 10 else startY + 10

                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                  self.colors[index], 2)
                    cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors[index], 2)
                    #time.sleep( 3 )
                    '''
                    cv2.rectangle(frame, (x+10,y+5), (w+10,h+5), (255,0,0), 2)
                    cv2.putText(frame, class_names[idx_max], (x+5, y-15),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            
                camera_run(1,face,label)
            cv2.imshow('frame', frame)
            fps.update()
                #time.sleep( 5 )
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cv2.destroyAllWindows()
                vs.stop()
                fps.stop()
                break
            
        # print("Fps: {:.2f}".format(fps.fps()))
        fps.update()
        # # yield L
        