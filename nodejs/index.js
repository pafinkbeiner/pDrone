const { Server } = require("socket.io");
const rpio = require("rpio");

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

//{ 
//    gyro_xyz: { x: -15, y: 12, z: -19 },
//    accel_xyz: { x: -512, y: 1136, z: 16176 },
//    rollpitch: { roll: 3.125, pitch: -6.93359375 } 
//} 
const stabilisation = async() => {
    return {
        vl: 0,
        vr: 0,
        hl: 0,
        hr: 0
    }
}

const init = () => {    
    console.log("Initializing...");
    let PWM_VL = new PWM(12, 15625).setup();
    let PWM_VR = new PWM(32, 15625).setup();
    let PWM_HL = new PWM(33, 15625).setup();
    let PWM_HR = new PWM(35, 15625).setup();
    console.log("Initialized!");

    return {
        PWM_VL,
        PWM_VR,
        PWM_HL,
        PWM_HR
    }
}

const arm = () => {

}

const calibrate = () => {

}

const flight = () => {
    
    console.log("Flight started");

    while(application.onFlight){

        console.log("onFLight is true");

        setTimeout(async () => {
            // get gyro information
            const gyroData = await update_telemetry();
            // get stabilisation values
            const stabData = await stabilisation(gyroData);
            // update motor values
            motor = {
                vl: stabData.vl + command.vl,
                vr: stabData.vr + command.vr,
                hl: stabData.hl + command.hl,
                hr: stabData.hr + command.hr
            }
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

rpio.init({
    mapping: 'physical',
    gpiomem: false,
    mock: false
});

rpio.open(15, rpio.INPUT);
console.log('Pin 15 is currently ' + (rpio.read(15) ? 'high' : 'low'));
rpio.open(12, rpio.PWM);
rpio.pwmSetClockDivider(64);
rpio.pwmSetRange(12, 1024);
rpio.pwmSetData(12, 512);

//var { PWM_VL, PWM_VR, PWM_HL, PWM_HR } = init();

setInterval(() => {
    console.log(update_telemetry());
}, 1000);

console.log("Server starting on Port: 8080");
io.listen(8080)