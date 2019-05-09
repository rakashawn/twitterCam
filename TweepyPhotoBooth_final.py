#!/usr/bin/env python
# https://www.instructables.com/id/Retro-Raspberry-Pi-Tumblr-GIF-Camera/
# https://www.instructables.com/id/Raspberry-Pi-Tumblr-GIF-Photo-Booth/
# https://picamera.readthedocs.io/en/release-1.10/recipes1.html
#import modules
import RPi.GPIO as GPIO
from time import sleep
import os
import picamera
import tweepy
from fractions import Fraction
import time
#timestamp
#from datetime import datetime
#define timestamp
#timestamp=datetime.now()

#create variables to hold commands
image_path = "/home/pi/Downloads/"
image_filename = "animation.gif" #path of the image" example  "/Users/nebulas/Desktop/latest.gif"
makeVid = "convert -delay 50 %s/image*.jpg %s/%s"%(image_path, image_path, image_filename)
displayGIF = "animate -loop 3 %s/%s &"%(image_path, image_filename)
shutdownCommand = "sudo shutdown -h now"
#meow3 = "mpg321 sounds/meow3.mp3"
#meow2 = "mpg321 sounds/meow2.mp3"

#create variables to hold pin numbers
readyLED = 21 # was 22; green LED
captureLED = 16 # was 17; white LED
processingLED = 20 # was 27; red LED
uploadingLED = 12 # new; wanted a different color for uploading
shutdownPIN = 17
button = 18 #stays
#from original code
#yellowLed = 17
#blueLed = 27


# Tweet Using python - Tweepy
# personal details
consumer_key = "your consumer_key"
consumer_secret = "your consumer_secret"
access_token = "your access_token"
access_token_secret = "your access_token_secret"

#Authentication of consumer key and secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

#Authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# end of Tweepy setup


camera = picamera.PiCamera() #initiate picamera module and class
camera.resolution = (640, 480) #set resolution of picture here
camera.brightness = 60 #set brightness settings to help with dark photos
camera.annotate_foreground = picamera.Color(y=0.2, u=0, v=0) #set color of annotation


print('Waiting for input...')
while True:
    try:
        #read button
        while True:
            #set up pins
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(shutdownPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(readyLED, GPIO.OUT)
            GPIO.setup(processingLED, GPIO.OUT)
            GPIO.setup(captureLED, GPIO.OUT)
            GPIO.setup(uploadingLED, GPIO.OUT)
            GPIO.output(readyLED, False)
            GPIO.output(processingLED, False)
            GPIO.output(captureLED, False)
            GPIO.output(uploadingLED, False)
            os.environ['DISPLAY'] = ':0'

            if GPIO.input(shutdownPIN) == False:
                print("Shutting system down...")
                os.system(shutdownCommand)
            if GPIO.input(button) == False:
                print('Button Pressed')
                #start camera preview
                camera.start_preview()
                #display text over preview screen
                camera.annotate_text = 'Get Ready!'

                #if pressed blink green LED at two speeds
                for i in range(3):
                    GPIO.output(readyLED, True)
                    sleep(1)
                    GPIO.output(readyLED, False)
                    sleep(1)
                for i in range(3):
                    GPIO.output(readyLED, True)
                    sleep(0.25)
                    GPIO.output(readyLED, False)
                    sleep(0.25)


                camera.annotate_text = '1'
                GPIO.output(captureLED, True)

                #take 6 photos
                for i, filename in enumerate(camera.capture_continuous(image_path+'image{counter:02d}.jpg')):
                    #sleep(0.5)
                    if i == 1:
                        camera.annotate_text = '2'
                        GPIO.output(captureLED, False)
                        sleep(0.5)
                        GPIO.output(captureLED, True)
                    elif i == 2:
                        camera.annotate_text = '3'
                        GPIO.output(captureLED, False)
                        sleep(0.5)
                        GPIO.output(captureLED, True)
                    elif i == 3:
                        camera.annotate_text = '4'
                        GPIO.output(captureLED, False)
                        sleep(0.5)
                        GPIO.output(captureLED, True)
                    elif i == 4:
                        camera.annotate_text = '5'
                        GPIO.output(captureLED, False)
                        sleep(0.5)
                        GPIO.output(captureLED, True)
                    elif i == 5:
                        camera.annotate_text = '6'
                        GPIO.output(captureLED, False)
                        sleep(0.5)
                        GPIO.output(captureLED, True)
                    if i == 6:
                        break
                GPIO.output(captureLED, False)
                camera.stop_preview() #stop preview
                print('converting to GIF')
                GPIO.output(processingLED, True)
                try:
                    os.system(makeVid) #send command to convert images to GIF
                except:
                    print("Make GIF didn't work.   Uhhhh.  Dunno what happened...")
                GPIO.output(processingLED, False)
                try:
                    os.system(displayGIF)
                except:
                    print("displayGIF didn't work.  Uhhhh.  Dunno what happend...")
                print('uploading') #let us know photo is about to start uploading
                GPIO.output(uploadingLED, True)
                #api = tweepy.API(auth)
                currentTime = str(time.strftime("%a_-_%H:%M:%S_%p"))
                tweet = "Animated Gif Raspberry Pi Camera! " + currentTime
                try:
                    status = api.update_with_media(image_path+image_filename, tweet)
                    api.update_status(status)
                except:
                    print("twitter reported error, but probably worked anyway...")
                print("uploaded") #let us know GIF has been uploaded
                GPIO.output(uploadingLED, False)
                #turn on uploaded LED and play meow samples
                #os.system(meow2)
                #sleep(0.25)
                #os.system(meow2)
                oldFile = image_path+image_filename
                newFile = image_path+"animation_"+currentTime+".gif"
                print("Copying %s to %s"%(oldFile, newFile))
                os.rename(oldFile, newFile)
                #print("Deleting old jpg files...")
                #for i in range(6):
                #    os.remove('%s/image%2d.jpg'%(image_path,i))
                print("check Twitter @yourtwitterhandle")
                print("Waiting for input...")

            GPIO.cleanup() #cleanup GPIO channels

    # hit Ctrl + C to stop program
    except:
        print ('program stopped')
        print('Waiting for input...')
