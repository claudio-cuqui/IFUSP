## program re-written by Claudio Cuqui (claudio.cuqui at usp dot br) and Felipe de Matos Melo (felipe.matosmelo at gmail dot com) 3th Dec 2015
## Strongly based on Shane Ormonde´s code  7th sept 2013
## Calculates the distance of a red dot in the field of view of the webcam.

import cv2
from numpy import *
import math
import os
import sys

#variables
loop = 1

dot_dist = 0

cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)

#Brightness Control - deprecated - v4l2-ctl now
#vc.set (CV2_CAP_PROP_BRIGHTNESS, 10)

if vc.isOpened(): # try to get the first frame
  rval, frame = vc.read()
else:
  rval = False
  print "failed to open webcam"
	

if rval == 1 :
  os.system('clear')
  while loop == 1:
    rval, frame = vc.read()
    #rval, original_frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
      loop = 0

    #Brightness Control
    #frame = (original_frame*0.7).astype(uint8)
     
    num = (frame[...,...,2] > 230)

    data = copy(num);

    # Exclusion matrix
    data[0:240,0:640]=False
    data[241:480,0:325]=False
    data[241:480,350:640]=False

    xy_val =  data.nonzero()

    y_val = median(xy_val[0])
    x_val = median(xy_val[1])

    dist = ((x_val - 320)**2 + (y_val - 240)**2 )**0.5 # distance of dot from center pixel
			
    # work out distance using D = h/tan(theta)
			
    # rpp and offset 
    theta = (0.00156*dist+0.013)
    tan_theta = math.tan(theta)

    if tan_theta > 0: # bit of error checking
      # h = 6.50
      obj_dist =  (int(6.5 / tan_theta)) 

      subtitle = " dist from center: " + str(int(dist)) + " pixels (" + str(int(x_val)) + "," + str(int(y_val)) + ") Objetct: "  + str(obj_dist) + "cm away" 
      cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      cv2.circle(frame, (int(x_val), int(y_val)), 10, (0, 0, 0), 2)
      cv2.putText(frame, subtitle , (5,470), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
      cv2.imshow("preview", frame)
    else:
      cv2.putText(frame, "Laser dot not found !"  , (5,470), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
      cv2.imshow("preview", frame)
