import RPi.GPIO as GPIO
import time

MAX_PWM_SPEED = 2000
MIN_PWM_SPEED = 1510

pwm_pins = {
    "vl": 33,
    "hl": 35,
    "vr": 12,
    "hr": 32
}

ledpin = pwm_pins["vr"]				    
GPIO.setwarnings(False)			        
GPIO.setmode(GPIO.BOARD)		        
GPIO.setup(ledpin,GPIO.OUT)


# # start pwm
pi_pwm = GPIO.PWM(ledpin, 16000)
pi_pwm.start(0)				      
pi_pwm.ChangeDutyCycle(75)
time.sleep(3)
        
