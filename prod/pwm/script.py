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
pi_pwm = GPIO.PWM(ledpin, 50)
pi_pwm.start(0)				      

def set_motor_speed(speed):
    # Begrenze den Wertebereich auf 0-100
    speed = max(0, min(abs(speed), 100))
    # Setze die PWM-Duty-Cycle basierend auf der Geschwindigkeit
    pi_pwm.ChangeDutyCycle(speed)


set_motor_speed(50)
time.sleep(2)

# Motor anhalten
set_motor_speed(0)

# Aufräumen und GPIO-Pins freigeben
pi_pwm.stop()
GPIO.cleanup()
