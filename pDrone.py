# pip install python-socketio
# pip install pymitter

# import local files
# import calibrate
import gyro
# import distance

# import libraries
import multiprocessing as mp
from pymitter import EventEmitter
import sys
import socketio
import time

# create a Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)

# create event emitter
emitter = EventEmitter()

# global control variables
control = {
    'vl': 0,
    'vr': 0,
    'hl': 0,
    'hr': 0    
}

# custom control event
@sio.on('control')
def another_event(sid, data):
    print("Custom control event triggered")
    print(sid)
    print(data)
    pass

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
    emitter.emit("motorStateChanged")
    print("Updated motor values: ")
    print(motor)

# motor state changed listener
@emitter.on("motorStateChanged")
def motorStateChangedHandler(arg):
    print("handler1 called with", arg)


# basic socket io connection event
@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)
    if sid == None:
        raise ConnectionRefusedError('authentication failed')
    else: 
        sio.emit('eventid', {'data': 'Testdata'})

# basic socket io disconnect event
@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# stablilisation method gets gyro data and returns new motor speed
def stabilisation(x, y, z, prev = motor):
    """function(x,y,z) -> dict({'vl','vr','hl', 'hr'})"""
    print("Stabilisation..")
    return {'vl': 1520,'vr': 1600,'hl': 1550, 'hr': 1570}

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

print("Initialize motor...")
# check correctness of motors
if(True):
    print("motor working...")
else:
    print("motor not working shutting down...")
    sys.exit()

while True:
    # get gyro base information -> data & acc
    gyrod = gyro.get_scaled_x_y_z_out()
    gyroacc = gyro.get_scaled_acc_x_y_z_out()

    # get gyro rotation information
    rotx = gyro.get_x_rotation(gyroacc['x'],gyroacc['y'],gyroacc['z'])
    roty = gyro.get_y_rotation(gyroacc['x'],gyroacc['y'],gyroacc['z'])

    # get new stabilasation values
    new = stabilisation(gyrod['x'], gyrod['y'], gyrod['z'])

    # set new values
    setMotorState(new)

    # debug
    time.sleep(2)



