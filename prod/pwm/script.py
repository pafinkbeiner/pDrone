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

# ledpin = pwm_pins["vr"]				    # PWM pin connected to LED
# GPIO.setwarnings(False)			        #disable warnings
# GPIO.setmode(GPIO.BOARD)		        #set pin numbering system
# GPIO.setup(ledpin,GPIO.OUT)


# # start pwm
# pi_pwm = GPIO.PWM(ledpin,1000)		    #create PWM instance with frequency
# pi_pwm.start(0)				            #start PWM of required Duty Cycle 
# pi_pwm.ChangeDutyCycle(50)
# pi_pwm.ChangeFrequency(5000)
# pi_pwm.ChangeFrequency(1000)

# for speed in range(2000, 15000, 1000):
#     pi_pwm.ChangeFrequency(speed)
#     time.sleep(3)
        

# motor_EN_A: Pin7         |  motor_EN_B: Pin11
# motor_A:  Pin8, Pin10    |  motor_B: Pin13, Pin12

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 14
Motor_A_Pin2  = 15
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

pwm_A = 0
pwm_B = 0

def setup():#Motor initialization
    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        pwm_B = GPIO.PWM(Motor_B_EN, 1000)
    except:
        pass

def motorStop():#Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)

def motor_right(status, direction, speed):#Motor 2 positive and negative rotation
    global  pwm_B
    if status == 0: # stop
        motorStop()
    else:
        if direction == Dir_forward:
            GPIO.output(Motor_B_Pin1, GPIO.HIGH)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            pwm_B.start(100)
            pwm_B.ChangeDutyCycle(speed)
        elif direction == Dir_backward:
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.HIGH)
            pwm_B.start(0)
            pwm_B.ChangeDutyCycle(speed)

def motor_left(status, direction, speed):# Motor 1 positive and negative rotation
    global pwm_A
    if status == 0: # stop
        motorStop()
    else:
        if direction == Dir_forward:#
            GPIO.output(Motor_A_Pin1, GPIO.HIGH)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            pwm_A.start(100)
            pwm_A.ChangeDutyCycle(speed)
        elif direction == Dir_backward:
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.HIGH)
            pwm_A.start(0)
            pwm_A.ChangeDutyCycle(speed)
    return direction


def destroy():

    motorStop()
    GPIO.cleanup()             # Release resource


try:
    pass
except KeyboardInterrupt:
    destroy()