use tonic::{transport::Server, Request, Response, Status};

use hello::greeter_server::{Greeter, GreeterServer};
use hello::{HelloReply, HelloRequest};

use gyro::gyro_server::{Gyro, GyroServer};
use gyro::{GyroReply, GyroRequest};

pub mod hello {
    tonic::include_proto!("hello");
}

pub mod gyro {
    tonic::include_proto!("gyro");
}

#[derive(Debug, Default)]
pub struct GyroService {}

#[derive(Debug, Default)]
pub struct MyGreeter {}

#[tonic::async_trait]
impl Greeter for MyGreeter {
    async fn say_hello(&self, request: Request<HelloRequest>) -> Result<Response<HelloReply>, Status> {
        println!("Got a request: {:?}", request);

        let reply = hello::HelloReply {
            message: format!("Hello {}!", request.into_inner().name).into(),
        };

        Ok(Response::new(reply))
    }
}

#[tonic::async_trait]
impl Gyro for GyroService {
    async fn stream_gyro_values(&self, request: Request<GyroRequest>) -> Result<Response<GyroReply>, Status> {
        println!("Got Request: {:?}", request);
        let reply = gyro::GyroReply {
            success: true
        };
        Ok(Response::new(reply))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let greeter = MyGreeter::default();
    let gyro = GyroService::default();

    Server::builder()
        .add_service(GreeterServer::new(greeter))
        .add_service(GyroServer::new(gyro))
        .serve(addr)
        .await?;

    Ok(())
}