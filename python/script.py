from __future__ import print_function

import logging

import grpc
import grpc_libs.hello_pb2 as hello_pb2
import grpc_libs.hello_pb2_grpc as hello_pb2_grpc

def run():
    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
