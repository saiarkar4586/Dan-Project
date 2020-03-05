import os
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sen = 7
GPIO.setup(sen, GPIO.IN, pull_up_down = GPIO.PUD_UP)
sensor = " "
while True:
           if GPIO.input(sen) == False:
                    sensor = "Liquid_level= 0"
           else:
                    sensor = "Liquid_level= 1"
	   print(sensor)
           sleep(1);
