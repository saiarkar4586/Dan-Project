#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_servo = 21
BUZZER= 23

buzzState = False
GPIO.setup(BUZZER, GPIO.OUT)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#servo_pin_out
GPIO.setup(GPIO_servo , GPIO.OUT)

p = GPIO.PWM(GPIO_servo , 50)
p.start(2.5)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if(dist<5):
                print ("Measured Distance = %.1f cm" % dist)
                print("Warning!! Water level is high ")
                GPIO.output(BUZZER,GPIO.HIGH)
                time.sleep(1)
		GPIO.output(BUZZER,GPIO.LOW)
		time.sleep(1)
		#servo_motor_open
		p.ChangeDutyCycle(12.5)
		print("Servo_motor_Open")

            else:
                print ("Measured Distance = %.1f cm" % dist)
                print("Water level is normal ")
		p.ChangeDutyCycle(2.5)
		print("Servo_motor_Close")
            time.sleep(4)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
	p.stop()
        GPIO.cleanup()


