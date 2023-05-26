from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory


factory = PiGPIOFactory()

servo = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

print("Start in the middle")
servo.mid()
sleep(1)
print("Go to min")
servo.min()
sleep(1)
print("Go to max")
servo.max()
sleep(1)
print("And back to middle")
servo.mid()
sleep(1)
servo.value = None

servo.value = -1
sleep(5)