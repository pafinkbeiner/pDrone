import pigpio  # importing GPIO library
import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because its too impatient
os.system("sudo pigpiod")  # Launching GPIO library
# As i said it is too impatient and so if this delay is removed you will get an error
time.sleep(1)

motor = {
    'vl': 13,
    'vr': 18,
    'hl': 19,
    'hr': 12
}

pi = pigpio.pi()

# set servo to 0 initially
pi.set_servo_pulsewidth(motor['vl'], 0)
pi.set_servo_pulsewidth(motor['vr'], 0)
pi.set_servo_pulsewidth(motor['hl'], 0)
pi.set_servo_pulsewidth(motor['hr'], 0)

max_value = 2000  # change this if your ESC's max value is different or leave it be
min_value = 1510  # change this if your ESC's min value is different or leave it be

print("Set max_value: "+str(max_value))
print("Set min_value: "+str(min_value))

def setServoSpeed(speed):
    pi.set_servo_pulsewidth(motor['vl'], speed['vl'])
    pi.set_servo_pulsewidth(motor['vr'], speed['vr'])
    pi.set_servo_pulsewidth(motor['hl'], speed['hl'])
    pi.set_servo_pulsewidth(motor['hr'], speed['hr'])

def calibrate():
    print("Started calibrate...")
    print("Setting motors to zero!")
    pi.set_servo_pulsewidth(motor['vl'], 0)
    pi.set_servo_pulsewidth(motor['vr'], 0)
    pi.set_servo_pulsewidth(motor['hl'], 0)
    pi.set_servo_pulsewidth(motor['hr'], 0)
    print("Disconnect the battery (7sec)")
    time.sleep(7)
    pi.set_servo_pulsewidth(motor['vl'], max_value)
    pi.set_servo_pulsewidth(motor['vr'], max_value)
    pi.set_servo_pulsewidth(motor['hl'], max_value)
    pi.set_servo_pulsewidth(motor['hr'], max_value)
    print("Connect the battery NOW.. (7sec)")
    time.sleep(7)
    pi.set_servo_pulsewidth(motor['vl'], min_value)
    pi.set_servo_pulsewidth(motor['vr'], min_value)
    pi.set_servo_pulsewidth(motor['hl'], min_value)
    pi.set_servo_pulsewidth(motor['hr'], min_value)
    print("Wait for 15 seconds")
    time.sleep(15)
    pi.set_servo_pulsewidth(motor['vl'], 0)
    pi.set_servo_pulsewidth(motor['vr'], 0)
    pi.set_servo_pulsewidth(motor['hl'], 0)
    pi.set_servo_pulsewidth(motor['hr'], 0)
    time.sleep(2)
    print("Arming ESC. Setting motor values to min value")
    pi.set_servo_pulsewidth(motor['vl'], min_value)
    pi.set_servo_pulsewidth(motor['vr'], min_value)
    pi.set_servo_pulsewidth(motor['hl'], min_value)
    pi.set_servo_pulsewidth(motor['hr'], min_value)
    time.sleep(1)
    print("Finished calibrating")
    return True


def arm():
    print("Connect the battery (7sec)")
    time.sleep(7)
    pi.set_servo_pulsewidth(motor['vl'], 0)
    pi.set_servo_pulsewidth(motor['vr'], 0)
    pi.set_servo_pulsewidth(motor['hl'], 0)
    pi.set_servo_pulsewidth(motor['hr'], 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(motor['vl'], max_value)
    pi.set_servo_pulsewidth(motor['vr'], max_value)
    pi.set_servo_pulsewidth(motor['hl'], max_value)
    pi.set_servo_pulsewidth(motor['hr'], max_value)
    time.sleep(1)
    pi.set_servo_pulsewidth(motor['vl'], min_value)
    pi.set_servo_pulsewidth(motor['vr'], min_value)
    pi.set_servo_pulsewidth(motor['hl'], min_value)
    pi.set_servo_pulsewidth(motor['hr'], min_value)
    time.sleep(1)
    return True

def stop(): 
    pi.set_servo_pulsewidth(motor['vl'], 0)
    pi.set_servo_pulsewidth(motor['vr'], 0)
    pi.set_servo_pulsewidth(motor['hl'], 0)
    pi.set_servo_pulsewidth(motor['hr'], 0)
    pi.stop()