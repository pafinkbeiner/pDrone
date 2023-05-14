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
# pi_pwm.ChangeDutyCycle(100)
# while True:
#     time.sleep(1)


# for speed in range(10, 100, 5):
#     print(speed)
#     pi_pwm.ChangeDutyCycle(speed)
#     time.sleep(3)

# pi_pwm.stop()
# pi_pwm.ChangeFrequency(1600)
# time.sleep(0.3)
# print(1600)
# pi_pwm.start(20)
# time.sleep(5)

for speed in range(1300, MAX_PWM_SPEED, 100):
    for duty in range(20, 50, 10):
        print("Speed: "+ str(speed) + " duty: "+ str(duty))
        pi_pwm.stop()
        pi_pwm.ChangeFrequency(speed)
        time.sleep(0.3)
        print(speed)
        pi_pwm.start(duty)
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