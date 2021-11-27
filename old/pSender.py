import socketio
import sys

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.on('motor')
def flight_data_handler(data):
    print("got something")
    print(data)

@sio.on('my message')
def on_message(data):
    print('I received a message!')

@sio.on('message')
def message(data):
    print('send worked got message!')

@sio.event
def disconnect():
    print('disconnected from server')

try: 
    print("Try to connect to socket.io server...")
    sio.connect('http://10.0.0.4:3000')
except:
    print("Could not connect! Exit application...")
    sys.exit()    

print("Connection successful!")

# command name: command
# data format: {"vl":5, "vr": 7, "hl": 3, "hr": 8}

while True:
    eventname = input("Eventname: ")
    data = input("Data: ")
    print("Emit information...")
    sio.emit(event = eventname, data=data)