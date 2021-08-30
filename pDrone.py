# pip install python-socketio

# import local files
# import control
# import gyro
# import distance

#import test files debug
from test import gyro_test as gyro
from test import control_test as control

# import libraries
import multiprocessing as mp
import sys
import socketio
import time
from aiohttp import web
import threading

# create a Socket.IO server
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

##################### MOTOR ########################

# global motor variables
motor = {
    'vl': 0,
    'vr': 0,
    'hl': 0,
    'hr': 0
}

# setter class for motor
def setMotorState(newState):
    motor.update(newState)
    print("Updated motor values: ", motor)

##################### COMMAND #####################

# global command variables
command = {
    'vl': 0,
    'vr': 0,
    'hl': 0,
    'hr': 0    
}

# custom control event
@sio.on('command')
async def another_event(sid, data):
    print("Custom command event triggered")
    print(sid)
    print(data)
    # update motor
    # setMotorState({
    #     'vl': motor['vl'] + data['vl'],
    #     'vr': motor['vr'] + data['vr'],
    #     'hl': motor['hl'] + data['hl'],
    #     'hr': motor['hr'] + data['hr']    
    # })
    # send back new motor state
    # sio.emit('motor', data=motor)
    pass

######################## MQTT BASIC ###########################

# basic socket io connection event
@sio.event
def connect(sid, environ):
    print('connect ', sid)
    # if sid == None:
    #     raise ConnectionRefusedError('authentication failed')
    # else: 
    #     sio.emit('eventid', data = { 'connection': "successful" })

# basic socket io disconnect event
@sio.event
def disconnect(sid):
    print('disconnect ', sid)  

######################## STABILIZATION ###########################

# stablilisation method gets gyro data and returns new motor speed
def stabilisation(x, y, z, prev = motor):
    """function(x,y,z,prev?) -> dict[str, Any]"""
    print("Stabilisation..")
    return {'vl': prev['vl'],'vr': prev['vr'],'hl': prev['hl'], 'hr': prev['hr']}

############################ MAIN ##############################

print("Starting control software...")
print("Available number of processors: ", mp.cpu_count())

print("Initialize gyro...")
# check correctness of gyro sensor
check1 = type(gyro.get_scaled_x_out()) == int or float
check2 = type(gyro.get_scaled_y_out()) == int or float
check3 = type(gyro.get_scaled_z_out()) == int or float
check4 = type(gyro.get_scaled_acc_x_out()) == int or float
check5 = type(gyro.get_scaled_acc_y_out()) == int or float
check6 = type(gyro.get_scaled_acc_z_out()) == int or float

if check1 and check2 and check3 and check4 and check5 and check6:
    print("gyro working...")
else:
    print("gyro not working shutting down...")
    sys.exit()

# check correctness of servo motors
print("Calibrate motor...")
check7 = control.calibrate()

print("Arming motor...")
check8 = control.arm()

if check7 and check8:
    print("motor working...")
else:
    print("motor not working shutting down...")
    sys.exit()

# starting mqtt server
print("Starting mqtt Server...")
try: 
    # todo start mqtt server on another thread
    web.run_app(app)
    # t = threading.Thread(target=handler)
    # t.start()
except:
    print("Could not connect! Exit application...")
    sys.exit()  

while True:
    # get gyro base information -> data & acc
    gyrod = gyro.get_scaled_x_y_z_out()
    gyroacc = gyro.get_scaled_acc_x_y_z_out()

    # get gyro rotation information
    rotx = gyro.get_x_rotation(gyroacc['x'],gyroacc['y'],gyroacc['z'])
    roty = gyro.get_y_rotation(gyroacc['x'],gyroacc['y'],gyroacc['z'])

    # get new stabilasation values
    stabRes = stabilisation(gyrod['x'], gyrod['y'], gyrod['z'], prev=motor)

    # set new values
    setMotorState(stabRes)

    # debug
    time.sleep(2)



