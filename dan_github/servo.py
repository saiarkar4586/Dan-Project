import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo_pin=40
GPIO.setup(servo_pin, GPIO.OUT)

p = GPIO.PWM(servo_pin, 50)

p.start(2.5)

try:
    while True:
        p.ChangeDutyCycle(12.5)  # turn towards 90 degree
        time.sleep(3) # sleep 1 second
        p.ChangeDutyCycle(2.5)  # turn towards 0 degree
        time.sleep(3) # sleep 1 second

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
