import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)			        
GPIO.setmode(GPIO.BOARD)		        
GPIO.setup(12, GPIO.OUT)


pi_pwm = GPIO.PWM(12, 50)
pi_pwm.start(0)				      

while True:
    for duty in range(0,101,1):
        pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
        time.sleep(0.01)
    time.sleep(0.5)
    
    for duty in range(100,-1,-1):
        pi_pwm.ChangeDutyCycle(duty)
        time.sleep(0.01)
    time.sleep(0.5)

pi_pwm.stop()
GPIO.cleanup()
