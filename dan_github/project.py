#Libraries
import pymongo
import RPi.GPIO as GPIO
import time
import datetime

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

#connect to mongodb
myclient = pymongo.MongoClient("mongodb+srv://root:root@cluster0-5sh5e.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["dan"]
mycol = mydb["water_level"]

def distance():

    GPIO.output(GPIO_TRIGGER, True)

    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if(dist<5):
		water_data = "%.1f"%dist
		water_level = float(water_data)
                print ("Measured Distance {} cm".format(water_level))
                print("Warning!! Water level is high ")
                GPIO.output(BUZZER,GPIO.HIGH)
                time.sleep(1)
	        GPIO.output(BUZZER,GPIO.LOW)
        	time.sleep(1)
        	#servo_motor_open
        	p.ChangeDutyCycle(12.5)
        	print("Servo_motor_Open")

		#insert data to mongodb
		currentDT = datetime.datetime.now()
		date =currentDT.strftime("%a, %b %d, %Y %I:%M:%S %p")

		mydict = {"Water Level":water_level , "Time":date}
		mycol.insert_one(mydict)

		print("Water Level is inserted in Mongodb")
		print(type(water_level))

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


