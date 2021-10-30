const { Server } = require("socket.io");

const dotenv = require("dotenv")
dotenv.config();

console.log("Firmware starting in "+process.env.ENV);

const update_telemetry = process.env.ENV == "production" ? require("./gyro") : require("./test/gyro.test");
const PWM = process.env.ENV == "production" ? require("./pwm") : require("./test/pwm.test");

const io = new Server();

const application = {
    onFlight: false
}

let motor = {
    vl: 1510,
    vr: 1510,
    hl: 1510,
    hr: 1510
}

let command = {
    vl: 0,
    vr: 0,
    hl: 0,
    hr: 0
}

console.log("Register listeners...");

io.on("connection", (socket) => {
    console.log("Client connected! Socket id: ", socket.id);
});

io.on("disconnect", (socket) => {
    console.log("Client disconnected!", socket.id);
});

io.on("command", (arg1) => {
    console.log("Command received: ", arg1);
    const data = JSON.parse(arg1);
    command = {
        vl: data['vl'],
        vr: data['vr'],
        hl: data['hl'],
        hr: data['hr']
    }
    io.emit("motor", JSON.stringify(motor));
});

io.on("flight", (arg1) => {
    console.log("Flight started: ", arg1);
    const data = JSON.parse(arg1);
    if(data['flight'] == 1){
        motor = {
            vl: 1510,
            vr: 1510,
            hl: 1510,
            hr: 1510
        }

        // start flight thread
        application.onFlight = true;
        flight();
        
    }else{

        application.onFlight = false;

    }

});

io.on("motor", () => io.emit("motor", JSON.stringify(motor)));

const stabilisation = () => {

}

const init = () => {

}

const arm = () => {

}

const calibrate = () => {

}

const flight = async() => {
    
    console.log("Flight started");

    while(application.onFlight){

        console.log("onFLight is true");

        setTimeout(() => {
            // get gyro information
            console.log(update_telemetry());
            // get stabilisation values

            // update motor values

            // set back command
            command = {
                vl: 0,
                vr: 0,
                hl: 0,
                hr: 0
            }
        }, 2000)
        
    }
}

setInterval(() => {
    console.log(update_telemetry());
}, 1000);

console.log("Server starting on Port: 8080");
io.listen(8080)