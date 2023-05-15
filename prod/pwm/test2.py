import time   
import pigpio 

ESC=18

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 700  #change this if your ESC's min value is different or leave it be

print("CALIBRATE")


print("ARM")
pi.set_servo_pulsewidth(ESC, 0)
time.sleep(1)
pi.set_servo_pulsewidth(ESC, max_value)
time.sleep(1)
pi.set_servo_pulsewidth(ESC, min_value)
time.sleep(1)

for speed in range(min_value, max_value, 100):
    print(speed)
    pi.set_servo_pulsewidth(ESC, speed)
    time.sleep(1)


pi.set_servo_pulsewidth(ESC, 0)
pi.stop()