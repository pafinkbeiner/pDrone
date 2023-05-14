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

ledpin = pwm_pins["hl"]				    # PWM pin connected to LED
GPIO.setwarnings(False)			        #disable warnings
GPIO.setmode(GPIO.BOARD)		        #set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)


# start pwm
pi_pwm = GPIO.PWM(ledpin,1000)		    #create PWM instance with frequency
pi_pwm.start(0)				            #start PWM of required Duty Cycle 

for speed in range(900, MAX_PWM_SPEED, 100):
    pi_pwm.stop()
    pi_pwm.ChangeFrequency(speed)
    time.sleep(0.3)
    print(speed)
    pi_pwm.start(50)
    time.sleep(3)

# set pwm to 1600
# pi_pwm.ChangeDutyCycle(1600)
# time.sleep(3)


# pi_pwm.ChangeDutyCycle(0)
# time.sleep(3)

# while True:
#     for duty in range(0,101,1):
#         pi_pwm.ChangeDutyCycle(duty)    #provide duty cycle in the range 0-100
#         time.sleep(0.01)
#     time.sleep(0.5)