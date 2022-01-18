#!/usr/bin/env python
#TrackingRobot3.py
from imgproc import * 
import RPi.GPIO as GPIO, time, os
shutdown=23
IN1=7
IN2=8
IN3=25
IN4=24
GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
p1 = GPIO.PWM(IN1, 500)  # channel=IN1 frequency=500Hz
p1.start(0)
p2 = GPIO.PWM(IN2, 500)  # channel=IN2 frequency=500Hz
p2.start(0)
p3 = GPIO.PWM(IN3, 500)  # channel=IN3 frequency=500Hz
p3.start(0)
p4 = GPIO.PWM(IN4, 500)  # channel=IN4 frequency=500Hz
p4.start(0)


# Create a camera 
cam = Camera(160,120) 

 # use the camera's width and height to set the viewer size 
view = Viewer(cam.width, cam.height, "Blob finding") 

while True:
        
        if(GPIO.input(shutdown)==1):
          os.system("sudo shutdown -h now")
                #sudo kill 2275 # kill on reboot

 
        # x and y position accumulators 
        acc_x = 0 
        acc_y = 0 

        # number of pixels accumulated 
        acc_count = 0 
 
        # grab an image from the camera 
        image = cam.grabImage()

         
        # iterate over every pixel 
        for x in range(image.width*0, image.width*1,5): 
                for y in range(image.height*0, image.height*1,5): 
                        # get the value of the current pixel 
                        red, green, blue = image[x, y]
                        #print 'red=',red,'  green=',green,'  blue=',blue

                        # check if the red intensity is greater than green and blue 
                        if red>200 or green>200 or blue>200:
                                # accumulate x and y of found pixel
                                acc_x += x 
                                acc_y += y 
                                # increment the accumulated pixels' count 
                                acc_count += 1 
                                # colour pixels which pass the test black 
                    
        # check the accumulator is greater than 0, to avoid a divide by 0
        if acc_count > 0: 
                # calculate the mean x and y positions 
                mean_x = acc_x / acc_count 
                mean_y = acc_y / acc_count 
                 
                # draw a small cross in red at the mean position 
                image[mean_x + 0, mean_y - 1] = 255, 0, 0 
                image[mean_x - 1, mean_y + 0] = 255, 0, 0 

                image[mean_x + 0, mean_y + 0] = 255, 0, 0 
                image[mean_x + 1, mean_y + 0] = 255, 0, 0 
                image[mean_x + 0, mean_y + 1] = 255, 0, 0 
                #print 'Xmean=',mean_x,'  Ymean=',mean_y
                                                                                                 
                view.displayImage(image)  #display the image on the viewer
                
                
                if mean_y<5:              # Too Close, stop robot  
                        p2.ChangeDutyCycle(0)
                        p3.ChangeDutyCycle(0)
                        
                        
               
                elif mean_x>=0 and mean_x<=160: #Robot centered, go forward
                        dcR=55+(mean_x-80)*50/80   # changed to 55
                        dcL=50-(mean_x-80)*50/80  
                        p2.ChangeDutyCycle(dcL)
                        p3.ChangeDutyCycle(dcR)

                        
                        
        else:                              # Stop Robot cuz cannot find target!
                p1.ChangeDutyCycle(0)
                p2.ChangeDutyCycle(0)
                p3.ChangeDutyCycle(0)
                 p4.ChangeDutyCycle(0)
                #GPIO.cleanup()
                print ('I cannot find target')
        


