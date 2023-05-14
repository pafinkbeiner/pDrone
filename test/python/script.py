from __future__ import print_function

import logging

import grpc
import hello_pb2
import hello_pb2_grpc
import gyro_pb2
import gyro_pb2_grpc

import libs.gyro_test as gyro

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        hello_stub = hello_pb2_grpc.GreeterStub(channel)
        gyro_stub = gyro_pb2_grpc.GyroStub(channel)
        response = hello_stub.SayHello(hello_pb2.HelloRequest(name='you'))
        gyro_values = gyro.get_scaled_acc_x_y_z_out()
        print(gyro_values)
        gyro_response = gyro_stub.StreamGyroValues(gyro_values)
        print(gyro_response.message)
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()
    run()
