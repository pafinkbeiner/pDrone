import os  # importing os library so as to communicate with the system
import time  # importing time library to make Rpi wait because its too impatient

time.sleep(1)

motor = {
    'vl': 4,
    'vr': 11,
    'hl': 10,
    'hr': 16
}


max_value = 2000  # change this if your ESC's max value is different or leave it be
min_value = 1510  # change this if your ESC's min value is different or leave it be

print("Set max_value: "+str(max_value))
print("Set min_value: "+str(min_value))

def setServoSpeed(speed):
    return None

def calibrate():
    print("Started calibrate...")
    print("Setting motors to zero!")
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        time.sleep(1)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':
            time.sleep(1)
            return True


def arm():
    print("Connect the battery and press Enter")
    inp=input()
    if inp == '':
        time.sleep(1)
        return True

def stop(): 
    return None