'''
It works with Raspberry Pi and servo motor.
'''

import RPi.GPIO as GPIO
import time, sys
from daemon import Daemon
import logging

def init_log(log_file):
	logging.basicConfig(filename='/var/log/%s'%(log_file),level=logging.INFO,
	 format="[%(asctime)s][%(levelname)s] %(message)s",
	 datefmt="%Y-%m-%d %H:%M:%S")


class MyDaemon(Daemon):


	def turn_right(self, servo):
		servo.ChangeDutyCycle(2.5)
		time.sleep(1)

	def turn_left(self, servo):
		servo.ChangeDutyCycle(12.5)
		time.sleep(1)

	def run(self, now=False):
		time_set=['08:00:00','18:30:00']
		led = 22
		while True:
			if time.strftime('%X') in time_set or now:
				try:
					GPIO.setmode(GPIO.BOARD)
					# pin 22 for servo
					GPIO.setup(15, GPIO.OUT)
					# pin 25 for led
					GPIO.setup(led, GPIO.OUT)
					GPIO.output(led, True)
					p = GPIO.PWM(15,50)
					p.start(1)
					self.turn_right(p)
					self.turn_left(p)
					GPIO.output(led,False)
					p.stop()
					GPIO.cleanup()
					logging.info("feeding.")
				except Exception, e:
					logging.error('%s' %e)

				time.sleep(1)
				if now:
					now=False
					exit()
		
	
init_log('%s.log' %sys.argv[0])

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/%s.pid'% sys.argv[0])

	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			logging.info("starting service")
			try:
				daemon.start()
			except Exception, e:
				logging.error("Shutting Down! %s" %e)

		elif 'stop' == sys.argv[1]:
			logging.info("stopping service")
			daemon.stop()

		elif 'restart' == sys.argv[1]:
			logging.info("restarting service")
			daemon.restart()

		elif 'status' == sys.argv[1]:
			pid = daemon.status()
			if pid:
				print "Service is running [pid:%s]" %pid
			else:
				print "Service is stopped!"

		elif 'now' == sys.argv[1]:
			daemon.run(now=True)

		else:
			print "Unknown command!"
			sys.exit(2)

		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|status" % sys.argv[0]
		sys.exit(2)
