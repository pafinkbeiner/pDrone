const { Server } = require("socket.io");
const update_telemetry = require("./gyro");

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

io.on("connection", (socket) => {
    console.log("Client connected! Socket id: ", socket.id);
});

io.on("disconnect", (socket) => {
    console.log("Client disconnected!", socket.id);
});

io.on("command", (arg1) => {
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
    
    while(application.onFlight){

        setTimeout(() => {
            // get gyro information

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

io.listen(3000)