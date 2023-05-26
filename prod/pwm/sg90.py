import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)			        
GPIO.setmode(GPIO.BOARD)		        
GPIO.setup(12,GPIO.OUT)


pi_pwm = GPIO.PWM(12, 50)
pi_pwm.start(0)				      

pi_pwm.ChangeDutyCycle(50)
time.sleep(3)

pi_pwm.stop()
GPIO.cleanup()
