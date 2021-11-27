# pip install python-socketio
# pip install aiohttp
# pip install asyncio

# import local files
# import control
# import gyro
# import distance
import wifi

# imports for infrared
import RPi.GPIO as GPIO

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


def irsetup():
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def binary_aquire(pin, duration):
    # aquires data as quickly as possible
    t0 = time()
    results = []
    while (time() - t0) < duration:
        results.append(GPIO.input(pin))
    return results


def on_ir_receive(pinNo, bouncetime=150):
    # when edge detect is called (which requires less CPU than constant
    # data acquisition), we acquire data as quickly as possible
    data = binary_aquire(pinNo, bouncetime/1000.0)
    if len(data) < bouncetime:
        return
    rate = len(data) / (bouncetime / 1000.0)
    pulses = []
    i_break = 0
    # detect run lengths using the acquisition rate to turn the times in to microseconds
    for i in range(1, len(data)):
        if (data[i] != data[i-1]) or (i == len(data)-1):
            pulses.append((data[i-1], int((i-i_break)/rate*1e6)))
            i_break = i
    # decode ( < 1 ms "1" pulse is a 1, > 1 ms "1" pulse is a 1, longer than 2 ms pulse is something else)
    # does not decode channel, which may be a piece of the information after the long 1 pulse in the middle
    outbin = ""
    for val, us in pulses:
        if val != 1:
            continue
        if outbin and us > 2000:
            break
        elif us < 1000:
            outbin += "0"
        elif 1000 < us < 2000:
            outbin += "1"
    try:
        return int(outbin, 2)
    except ValueError:
        # probably an empty code
        return None


def irdestroy():
    GPIO.cleanup()


def startIRListener():
    irsetup()
    print("IR is set up")
    try:
        while True:

            GPIO.wait_for_edge(11, GPIO.FALLING)
            code = on_ir_receive(11)
            if code:
                print(str(hex(code)))
                # hier muss der code von unten hin -> Exec IR Command
            else:
                print("Invalid code")

    except KeyboardInterrupt:
        pass
    except RuntimeError:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        pass
    print("Quitting")
    irdestroy()

def execIRCommand(hex):
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

################################## EXEC #####################################


# Threading
# add main loop to thread pool
t1 = threading.Thread(target=flight, name="Thread-1")
# add mqtt server thread to thread pool
t2 = threading.Thread(target=startIRListener, name="Thread-2")

t2.start()
