from __future__ import print_function

import logging

import grpc
import grpc_libs.hello_pb2 as hello_pb2
import grpc_libs.hello_pb2_grpc as hello_pb2_grpc
import grpc_libs.gyro_pb2 as gyro_pb2
import grpc_libs.gyro_pb2_grpc as gyro_pb2_grpc

import libs.gyro_test as gyro

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        hello_stub = hello_pb2_grpc.GreeterStub(channel)
        gyro_stub = gyro_pb2_grpc.GyroStub(channel)
        response = hello_stub.SayHello(hello_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()
    run()
