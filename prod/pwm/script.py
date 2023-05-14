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

pwm = GPIO.PWM(ledpin, 1000)

# Set up duty cycle range for motor controller
max_duty_cycle = 100
min_duty_cycle = 20

# Start PWM with 0 duty cycle
pwm.start(0)

# Gradually increase duty cycle to start motor
for duty_cycle in range(min_duty_cycle, max_duty_cycle+1, 5):
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)

# Change duty cycle to maintain motor speed
pwm.ChangeDutyCycle(50)
while True:
    time.sleep(1)

# Clean up GPIO pins
pwm.stop()
GPIO.cleanup()


# for speed in range(900, MAX_PWM_SPEED, 100):
#     for duty in range(10, 100, 10):
#         print("Speed: "+ str(speed) + " duty: "+ str(duty))
#         pi_pwm.stop()
#         pi_pwm.ChangeFrequency(speed)
#         time.sleep(0.3)
#         print(speed)
#         pi_pwm.start(duty)
#         time.sleep(1)

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