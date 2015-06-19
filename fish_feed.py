import RPi.GPIO as GPIO
import time

def turn_right(servo):
	servo.ChangeDutyCycle(2.5)
	time.sleep(1)
	#servo.ChangeDutyCycle(12.5)
	#servo.ChangeDutyCycle(12.5)
	#servo.ChangeDutyCycle(7.5)
	#servo.ChangeDutyCycle(2.5)
	#time.sleep(1)



def turn_left(servo):
	servo.ChangeDutyCycle(12.5)
	time.sleep(1)

time_set=['08:00:00','18:30:00']
led = 22
while True:
	if time.strftime('%X') in time_set:
		GPIO.setmode(GPIO.BOARD)
		# pin 22 for servo
		GPIO.setup(15, GPIO.OUT)
		
		# pin 25 for led
		GPIO.setup(led, GPIO.OUT)
		GPIO.output(led, True)
		p = GPIO.PWM(15,50)
		p.start(2.5)
		turn_right(p)
		turn_left(p)
		GPIO.output(led,False)
		GPIO.cleanup()
		#time.sleep(10)
		
	
