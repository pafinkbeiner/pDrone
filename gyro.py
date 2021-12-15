#!/usr/bin/python

# Activate I2C Bus
# sudo raspi-config > ...
# sudo apt-get install i2c-tools python-smbus
# sudo i2cdetect -y 1

# Pinbelegung (BCM)
# Pin 1 (3.3V)	VCC
# Pin 3 (SDA)	SDA
# Pin 5 (SCL)	SCL
# Pin 6 (GND)	GND

import smbus
import math
import time
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
#### unscaled ####
def get_x_out():
    return read_word_2c(0x43)

def get_y_out():
    return read_word_2c(0x45)

def get_z_out():
    return read_word_2c(0x47)


def get_acc_x_out():
    return read_word_2c(0x3b)

def get_acc_y_out():
    return read_word_2c(0x3d)

def get_acc_z_out():
    return read_word_2c(0x3f)

def get_acc_x_y_z_out():
    return { 'x': get_acc_x_out(), 'y': get_acc_y_out(), 'z': get_acc_z_out()}

#### scaled ####
def get_scaled_x_y_z_out():
    return { 'x': get_scaled_x_out(), 'y': get_scaled_y_out(), 'z': get_scaled_z_out()}

def get_scaled_x_out():
    return (read_word_2c(0x43) / 131)

def get_scaled_y_out():
    return (read_word_2c(0x45) / 131)

def get_scaled_z_out():
    return (read_word_2c(0x47) / 131)

def get_scaled_acc_x_y_z_out():
    return { 'x': get_scaled_acc_x_out(), 'y': get_scaled_acc_y_out(), 'z': get_scaled_acc_z_out()}

def get_scaled_acc_x_out():
    return (read_word_2c(0x3b) / 16384.0)

def get_scaled_acc_y_out():
    return (read_word_2c(0x3d) / 16384.0)

def get_scaled_acc_z_out():
    return (read_word_2c(0x3f) / 16384.0)

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)
 
# print( "Gyroskop")
# print( "--------")
 
# gyroskop_xout = read_word_2c(0x43)
# gyroskop_yout = read_word_2c(0x45)
# gyroskop_zout = read_word_2c(0x47)
 
# print( "gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131))
# print( "gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131))
# print( "gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131))
 
# print
# print ("Beschleunigungssensor")
# print ("---------------------")
 
# beschleunigung_xout = read_word_2c(0x3b)
# beschleunigung_yout = read_word_2c(0x3d)
# beschleunigung_zout = read_word_2c(0x3f)
 
# beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
# beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
# beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
 
# print ("beschleunigung_xout: ", ("%6d" % beschleunigung_xout), " skaliert: ", beschleunigung_xout_skaliert)
# print ("beschleunigung_yout: ", ("%6d" % beschleunigung_yout), " skaliert: ", beschleunigung_yout_skaliert)
# print ("beschleunigung_zout: ", ("%6d" % beschleunigung_zout), " skaliert: ", beschleunigung_zout_skaliert)
 
# print ("X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
# print ("Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))

# while True:
#     print("Sensor X: "+str(read_word_2c(0x43)))
#     print("Sensor X: "+str(read_word_2c(0x45)))
#     print("Sensor X: "+str(read_word_2c(0x47)))
#     print ("X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
#     print ("Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
#     time.sleep(1)
#     print("---------------------------------------")