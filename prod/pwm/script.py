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

ledpin = pwm_pins["vr"]				    # PWM pin connected to LED
GPIO.setwarnings(False)			        #disable warnings
GPIO.setmode(GPIO.BOARD)		        #set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)


# start pwm
pi_pwm = GPIO.PWM(ledpin,1000)		    #create PWM instance with frequency
pi_pwm.start(0)				            #start PWM of required Duty Cycle 
pi_pwm.ChangeDutyCycle(50)
pi_pwm.ChangeFrequency(5000)
pi_pwm.ChangeFrequency(1000)

for speed in range(2000, 15000, 1000):
    pi_pwm.ChangeFrequency(speed)
    time.sleep(3)
        


