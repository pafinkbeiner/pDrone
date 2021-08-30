import socketio
import sys

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

try: 
    print("Try to connect to socket.io server...")
    sio.connect('http://localhost:8080')
except:
    print("Could not connect! Exit application...")
    sys.exit()    

print("Connection successful!")

while True:
    eventname = input("Eventname: ")
    data = input("Data: ")
    print("Emit information...")
    sio.emit(event = eventname, data=data)