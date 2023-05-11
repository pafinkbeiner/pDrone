#!/usr/bin/python

import math 

def read_byte(reg):
    return 0.5
 
def read_word(reg):
    return 0.5
 
def read_word_2c(reg):
    return 0.5
 
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

