import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
channels=[i for i in xrange(27)]
GPIO.setup(channels,GPIO.OUT)
GPIO.output(channels,0)
