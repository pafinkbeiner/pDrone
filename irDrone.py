# pip install python-socketio
# pip install aiohttp
# pip install asyncio

# import local files
# import control
# import gyro
# import distance
import wifi

# imports for infra red
import socket, signal
import lirc 

# import test files debug
from test import gyro_test as gyro
from test import control_test as control

# import libraries
import concurrent.futures
import multiprocessing as mp
import sys
import time
import threading
import json

#################### IR ######################
Lirc = lirc.init("keys")

##################### MOTOR ########################

# global motor variables
motor = {
    'vl': 1510,
    'vr': 1510,
    'hl': 1510,
    'hr': 1510
}

# setter class for motor


def setMotorState(newState):
    motor.update(newState)
    print("Updated motor values: ", motor)
    # sio.send(json.dumps(motor))


##################### COMMAND #####################

# global command variables
command = {
    'vl': 0,
    'vr': 0,
    'hl': 0,
    'hr': 0
}

######################## Application Data ########################

application = {
    'onFlight': False
}

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


def stabilisation(x, y, z, prev=motor):
    """function(x,y,z,prev?) -> dict[str, Any]"""
    print("Stabilisation..")
    return {'vl': prev['vl'], 'vr': prev['vr'], 'hl': prev['hl'], 'hr': prev['hr']}

############################ MAIN ##############################


def init():
    print("Available number of processors: ", mp.cpu_count())

    print("Starting Access Point")
    # start wifi
    # wifi.access_point.start()

    # stop
    # access_point.stop()

    print("Initialize gyro...")
    # check correctness of gyro sensor
    check1 = type(gyro.get_scaled_x_out()) == int or float
    check2 = type(gyro.get_scaled_y_out()) == int or float
    check3 = type(gyro.get_scaled_z_out()) == int or float
    check4 = type(gyro.get_scaled_acc_x_out()) == int or float
    check5 = type(gyro.get_scaled_acc_y_out()) == int or float
    check6 = type(gyro.get_scaled_acc_z_out()) == int or float

    if check1 and check2 and check3 and check4 and check5 and check6:
        return True
    else:
        return False


def arm():
    print("Arming motor...")
    check8 = control.arm()
    return check8


def calibrate():
    print("Calibrate motor...")
    check7 = control.calibrate()
    return check7


def flight():

    while True:

        # stops current thread
        if application['onFlight'] == True:

            last_time = round(time.time() * 1000)

            # get gyro base information -> data & acc
            gyrod = gyro.get_scaled_x_y_z_out()
            gyroacc = gyro.get_scaled_acc_x_y_z_out()

            # get gyro rotation information
            rotx = gyro.get_x_rotation(
                gyroacc['x'], gyroacc['y'], gyroacc['z'])
            roty = gyro.get_y_rotation(
                gyroacc['x'], gyroacc['y'], gyroacc['z'])

            # get new stabilasation values
            stabRes = stabilisation(
                gyrod['x'], gyrod['y'], gyrod['z'], prev=motor)

            # refresh motor state with control values and stabilist values
            setMotorState({
                'vl': stabRes['vl'] + command['vl'],
                'vr': stabRes['vr'] + command['vr'],
                'hl': stabRes['hl'] + command['hl'],
                'hr': stabRes['hr'] + command['hr']
            })

            # set back control state after changing
            command.update({
                'vl': 0,
                'vr': 0,
                'hl': 0,
                'hr': 0
            })

            print("Took: "+str(round(time.time() * 1000) - last_time)+"ms")

        # debug
        time.sleep(2)


def startIRListener():

    while True:

        print("Listening on IR Commands: ")
        out = lirc.nextcode()
        cmd = out[0]
        print(cmd)
        command = "test"

        # GET OPERATIONAL COMMAND
        if command == "init":
            init()
        elif command == "arm":
            arm()
        elif command == "calibrate":
            calibrate()
        # GET PLUS COMMAND
        elif command == "VL+":
            command.update({
                'vl': 10,
                'vr': 0,
                'hl': 0,
                'hr': 0
            })
        elif command == "VR+":
            command.update({
                'vl': 0,
                'vr': 10,
                'hl': 0,
                'hr': 0
            })
        elif command == "HL+":
            command.update({
                'vl': 0,
                'vr': 0,
                'hl': 10,
                'hr': 0
            })
        elif command == "HR+":
            command.update({
                'vl': 0,
                'vr': 0,
                'hl': 0,
                'hr': 10
            })
        # GET MINUS COMMAND
        elif command == "VL-":
            command.update({
                'vl': -10,
                'vr': 0,
                'hl': 0,
                'hr': 0
            })
        elif command == "VR-":
            command.update({
                'vl': 0,
                'vr': -10,
                'hl': 0,
                'hr': 0
            })
        elif command == "HL-":
            command.update({
                'vl': 0,
                'vr': 0,
                'hl': -10,
                'hr': 0
            })
        elif command == "HR-":
            command.update({
                'vl': 0,
                'vr': 0,
                'hl': 0,
                'hr': -10
            })
        # GET FLIGHT COMMAND
        elif command == "SFLIGHT":
            # set motor to default before starting
            motor.update({
                'vl': 1510,
                'vr': 1510,
                'hl': 1510,
                'hr': 1510
            })
            # start thread - if not already
            if t1.is_alive() == False:
                application['onFlight'] = True
                t1.start()
            else:
                application['onFlight'] = True

        elif command == "EFLIGHT":
            # stop flight thread
            application['onFlight'] = False

        time.sleep(1)

################################## EXEC #####################################


# Threading
# add main loop to thread pool
t1 = threading.Thread(target=flight, name="Thread-1")
# add mqtt server thread to thread pool
t2 = threading.Thread(target=startIRListener, name="Thread-2")

t2.start()
