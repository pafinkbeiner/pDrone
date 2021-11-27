from flask import Flask
from flask import request
import time
import json
import logging
from PyAccessPoint import pyaccesspoint
from threading import Thread
import sys
import os
import control as control
import gyro as gyro


###################### init ####################
app = Flask(__name__)
access_point = pyaccesspoint.AccessPoint(wlan="wlan0", ssid="drone", password="12345678", netmask="255.255.255.252", ip="10.0.0.1")
access_point.start()
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(
                        os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger()
port = 8080
application = {
    'onFlight': False,
    'stabilisationRate': 2
}
command = {
    'vl': 0,
    'vr': 0,
    'hl': 0,
    'hr': 0
}
motor = {
    'vl': 1510,
    'vr': 1510,
    'hl': 1510,
    'hr': 1510
}
gyroBase = {
    "x": 0,
    "y": 0,
    "z": 0
}

###################### main ####################


def setMotorState(newState):
    motor.update(newState)
    print("Updated motor values: ", motor)


def initialize():
    logger.log(1, "Initialize Startup Sequence")
    check0 = True
    if os.environ.get("env") == "production":
        check0 = access_point.is_running()

    logger.log(1, "Initialize gyro...")
    # check correctness of gyro sensor
    check1 = type(gyro.get_scaled_x_out()) == int or float
    check2 = type(gyro.get_scaled_y_out()) == int or float
    check3 = type(gyro.get_scaled_z_out()) == int or float
    check4 = type(gyro.get_scaled_acc_x_out()) == int or float
    check5 = type(gyro.get_scaled_acc_y_out()) == int or float
    check6 = type(gyro.get_scaled_acc_z_out()) == int or float

    # set current gyro position as default
    gyroBase.update({
        "x": gyro.get_scaled_x_out(),
        "y": gyro.get_scaled_y_out(),
        "z": gyro.get_scaled_z_out(),
        "x_s": gyro.get_scaled_acc_x_out(),
        "y_s": gyro.get_scaled_acc_y_out(),
        "z_s": gyro.get_scaled_acc_z_out()
    })

    if check0 and check1 and check2 and check3 and check4 and check5 and check6:
        logger.log(1, "Startup performed successfully")
        return True
    else:
        logger.log(1, "Error occured while checking system")
        return False


def calibrate():
    logger.log(1, "Initialize Calibrate")
    check7 = control.calibrate()
    return check7


def arm():
    logger.log(1, "Initialize arm")
    check8 = control.arm()
    return check8


def stabilisation(x, y, z, prev=motor):
    print("Stabilisation..")
    # use access to gyroBase

    return {'vl': prev['vl'], 'vr': prev['vr'], 'hl': prev['hl'], 'hr': prev['hr']}


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

            control.setMotorState(motor)

            # set back control state after changing
            command.update({
                'vl': 0,
                'vr': 0,
                'hl': 0,
                'hr': 0
            })

            print("Took: "+str(round(time.time() * 1000) - last_time)+"ms")

        time.sleep(application["stabilisationRate"])


def start_app():
    app.run(host='0.0.0.0', port=port, debug=False)


#################### threads ###################
t1 = Thread(target=flight, name="Flight")
t2 = Thread(target=start_app, name="Flask")

##################### routes ###################


@app.route("/")
def home_route():
    return json.dumps({
        "routes": ["/init", "/command", "/command/<key>/<value>", "flight/<b>"]
    })


@app.route("/init")
def init_route():
    res = initialize()
    return json.dumps(res)

@app.route("/calibrate")
def calibrate_route():
    res = control.calibrate()
    return json.dumps("true")

@app.route("/arm")
def arm_route():
    res = control.arm()
    return json.dumps("true")

@app.route("/command", methods=['POST'])
def command_route():
    parsedData = request.data
    print(parsedData)
    # update motor
    # command.update({
    #     'vl': parsedData['vl'],
    #     'vr': parsedData['vr'],
    #     'hl': parsedData['hl'],
    #     'hr': parsedData['hr']
    # })
    return json.dumps("Received")


@app.route("/command/<key>/<value>")
def command_alt_route(key, value):
    print(f'Received {key} and {value}')
    if key == "vl" or key == "vr" or key == "hl" or key == "hr":
        command.update({
            key: int(value)
        })
        return json.dumps("Received")
    else:
        return json.dumps("Wrong key")


# /flight/1 od. /flight/0
@app.route("/flight/<b>")
def flight_route(b):
    data = b
    if data == "1":
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
            return json.dumps("Started")
        else:
            application['onFlight'] = True
            return json.dumps("Started")
    else:
        # stop flight thread
        application['onFlight'] = False
        return json.dumps("Stopped")

@app.route("/kill")
def kill_route():
    sys.exit()

###################### prod #####################
t2.start()
