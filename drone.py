from flask import Flask
from flask import request
import time
import json
from threading import Thread
import sys
import os
from dotenv import load_dotenv
import direction
import stability

# load env for using env variables
load_dotenv()
if os.environ.get("env") == "production":
    from PyAccessPoint import pyaccesspoint
    import control as control
    import gyro as gyro
else:
    import control_test as control
    import gyro_test as gyro

###################### init ####################
app = Flask(__name__)
if os.environ.get("env") == "production":
    print("Starting Access Point...")
    access_point = pyaccesspoint.AccessPoint(
    wlan="wlan0", ssid="drone", password="12345678", netmask="255.255.255.252", ip="10.0.0.1")
    access_point.start()

print("Initialize global Variables...")

port = os.environ.get("port")
application = {
    'onFlight': False,
    'stabilisationRate': 0.2
}

maxCorrection = 30

maxCommand = 20
minCommand = maxCommand * (-1)
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
    "y": 0
}

###################### main ####################

def setMotorState(newState):
    motor.update(newState)
    print("Updated motor values: ", motor)

# set delta for command 
def setCommandState(newState):
    # it should always be: minCommand < newState['x'] < maxCommand
    # f.e. -5 < 1 < 5
    newvl = newState['vl']
    newvr = newState['vr']
    newhl = newState['hl']
    newhr = newState['hr']
    # check max value
    if newvl > maxCommand: newvl = maxCommand
    if newvr > maxCommand: newvr = maxCommand
    if newhl > maxCommand: newhl = maxCommand
    if newhr > maxCommand: newhr = maxCommand
    # check min value
    if newvl < minCommand: newvl = minCommand
    if newvr < minCommand: newvr = minCommand
    if newhl < minCommand: newhl = minCommand
    if newhr < minCommand: newhr = minCommand
    command.update({
        'vl': newvl,
        'vr': newvr,
        'hl': newhl,
        'hr': newhr
    })
    print("Updated command values: ", motor)

def initialize():

    print("Initializing...")
    # check accesss point status if run in production
    check0 = True
    if os.environ.get("env") == "production":
        check0 = access_point.is_running()

    # check correctness of gyro sensor
    check1 = type(gyro.get_scaled_x_out()) == int or float
    check2 = type(gyro.get_scaled_y_out()) == int or float
    check3 = type(gyro.get_scaled_z_out()) == int or float
    check4 = type(gyro.get_scaled_acc_x_out()) == int or float
    check5 = type(gyro.get_scaled_acc_y_out()) == int or float
    check6 = type(gyro.get_scaled_acc_z_out()) == int or float

    # set current gyro position as default
    calibrateGyro()

    if check0 and check1 and check2 and check3 and check4 and check5 and check6:
        return True
    else:
        return False


def calibrate():
    check7 = control.calibrate()
    return check7

def calibrateGyro():
    gyroBase.update({
        "x": gyro.get_acc_x_out(),
        "y": gyro.get_acc_y_out()
    })

def arm():
    check8 = control.arm()
    return check8


def flight():

    while True:

        # stops current thread
        if application['onFlight'] == True:

            last_time = round(time.time() * 1000)

            # get gyro base information -> data & acc
            gyroX = gyro.get_acc_x_out()
            gyroY = gyro.get_acc_y_out()

            # get new stabilasation values (motor delta)
            stabRes = stability.correct(gyroX, gyroY, gyroBase, maxCorrection)
            stabResNormalized = direction.normalize(stabRes)

            # refresh motor state with control values and stabilist values
            setMotorState({
                'vl': motor['vl'] + stabResNormalized['vl'] + command['vl'],
                'vr': motor['vr'] + stabResNormalized['vr'] + command['vr'],
                'hl': motor['hl'] + stabResNormalized['hl'] + command['hl'],
                'hr': motor['hr'] + stabResNormalized['hr'] + command['hr']
            })

            # set new motor speed on servos
            control.setServoSpeed(motor)

            # set back control state after changing - changing in the future
            setCommandState({
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
    parsedData = json.loads(request.data)
    # update motor
    setCommandState({
        'vl': parsedData['vl'],
        'vr': parsedData['vr'],
        'hl': parsedData['hl'],
        'hr': parsedData['hr']
    })
    return json.dumps("Received")

@app.route("/degree/<deg>/<max>/<force>")
def degree_route(deg, max, force):

    parsedDeg = float(deg)
    parsedMax = float(max)
    parsedForce = float(force)
    
    if (type(parsedDeg) == int or float) and (type(parsedMax) == int or float) and (type(parsedForce) == int or float):
        dta = direction.degree2motor(parsedDeg, parsedMax, parsedForce)
        normalized = direction.normalize(dta)
        setCommandState({
            'vl': normalized['vl'],
            'vr': normalized['vr'],
            'hl': normalized['hl'],
            'hr': normalized['hr']
        })
        return json.dumps("Received")
    else: 
        json.dumps("Wrong type!")

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
        control.stop()
        application['onFlight'] = False
        return json.dumps("Stopped")

@app.route("/kill")
def kill_route():
    sys.exit()

@app.route("/motor")
def motor_route():
    return json.dumps(motor)

###################### prod #####################
# start main program
initRes = initialize()
if initRes == True: print("Init Process sucessfull!")
# calibrate()
# debug
application['onFlight'] = True
flight()
t2.start()
