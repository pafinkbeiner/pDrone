# pip install python-socketio
# pip install aiohttp
# pip install asyncio

# import local files
# import control
# import gyro
# import distance
import wifi

#import test files debug
from test import gyro_test as gyro
from test import control_test as control

# import libraries
import concurrent.futures
import multiprocessing as mp
import sys
import socketio
import time
from aiohttp import web
import threading
import asyncio
import json

# create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode='aiohttp', async_handlers=True)
app = web.Application()
sio.attach(app)

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
def stabilisation(x, y, z, prev = motor):
    """function(x,y,z,prev?) -> dict[str, Any]"""
    print("Stabilisation..")
    return {'vl': prev['vl'],'vr': prev['vr'],'hl': prev['hl'], 'hr': prev['hr']}

############################ MAIN ##############################

def init():
    print("Available number of processors: ", mp.cpu_count())

    print("Starting Access Point")
    # start wifi
    # wifi.access_point.start()

    #stop
    #access_point.stop()

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
            rotx = gyro.get_x_rotation(gyroacc['x'],gyroacc['y'],gyroacc['z'])
            roty = gyro.get_y_rotation(gyroacc['x'],gyroacc['y'],gyroacc['z'])

            # get new stabilasation values
            stabRes = stabilisation(gyrod['x'], gyrod['y'], gyrod['z'], prev=motor)

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

def startMqttServer(mqttServer = app):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(web.run_app(mqttServer))
    loop.run_forever()

################################## EXEC #####################################


# Threading
# add main loop to thread pool
t1 = threading.Thread(target=flight, name="Thread-1")
# add mqtt server thread to thread pool
# t2 = threading.Thread(target=startMqttServer, args=(app,), name="Thread-2")

t1.start()

# start mqtt server


# Thread Pool
# executer = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# b = executer.submit(startMqttServer)

# a = executer.submit(flight)

################################### MQTT ##########################################

# init mqtt event
@sio.on('init')
async def onInitHandler(sid, data):
    init()
    pass

# init mqtt event
@sio.on('arm')
async def onArmHandler(sid, data):
    arm()
    pass

# init mqtt event
@sio.on('calibrate')
async def onCalibrateHandler(sid, data):
    calibrate()
    pass

# custom control event
@sio.on('command')
async def onCommandHandler(sid, data):
    print(sid)
    parsedData = json.loads(data)
    # update motor
    command.update({
        'vl': parsedData['vl'],
        'vr': parsedData['vr'],
        'hl': parsedData['hl'],
        'hr': parsedData['hr']
    })
    # send back new motor state
    await sio.emit("motor", json.loads(motor))
    pass

# start flight loop
@sio.on('flight')
async def onFlighHandler(sid, data):
    data = json.loads(data)
    if data['flight'] == "1":
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
    else:
        # stop flight thread
        application['onFlight'] = False

# get motor information
@sio.on('motor')
async def onMotorHandler(sid, data):
    await sio.emit("motor", json.dumps(motor))
    pass













