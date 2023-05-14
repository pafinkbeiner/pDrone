use std::{thread::spawn, sync::mpsc::channel};

const MAX_MOTOR: i32 = 2499;
const MAX_COMMAND: i32 = 20;
const MIN_COMMAND: i32 = MAX_COMMAND  * (-1);
const MAX_CORRECTION: i32 = 30;

struct Motor {
    vl: i32,
    vr: i32,
    hl: i32,
    hr: i32,
}

impl Motor {
    fn set_motor_state(&mut self, vl: i32, vr: i32, hl: i32, hr: i32) {
        if vl > MAX_MOTOR { self.vl = MAX_MOTOR } else { self.vl = vl };
        if vr > MAX_MOTOR { self.vr = MAX_MOTOR } else { self.vr = vr };
        if hl > MAX_MOTOR { self.hl = MAX_MOTOR } else { self.hl = hl };
        if hr > MAX_MOTOR { self.hr = MAX_MOTOR } else { self.hr = hr };
    }
}

struct Command {
    vl: i32,
    vr: i32,
    hl: i32,
    hr: i32,
}

impl Command {
    fn set_command_state(&mut self, vl: i32, vr: i32, hl: i32, hr: i32) {
        if vl > MAX_COMMAND {
            self.vl = MAX_COMMAND;
        }else if vl < MIN_COMMAND {
            self.vl = MIN_COMMAND;
        }else{
            self.vl = vl;
        }
        if vr > MAX_COMMAND {
            self.vr = MAX_COMMAND;
        }else if vr < MIN_COMMAND {
            self.vr = MIN_COMMAND;
        }else{
            self.vr = vr;
        }
        if hl > MAX_COMMAND {
            self.hl = MAX_COMMAND;
        }else if hl < MIN_COMMAND {
            self.hl = MIN_COMMAND;
        }else{
            self.hl = hl;
        }
        if hr > MAX_COMMAND {
            self.hr = MAX_COMMAND;
        }else if hr < MIN_COMMAND {
            self.hr = MIN_COMMAND;
        }else{
            self.hr = hr;
        }
    }
}

struct GyroBase {
    x: i32,
    y: i32
}

fn initialize() {
    println!("Initialize Drone...")
}

fn main() {
    initialize();

    // let (tx, rx) = channel::<String>();

    let sender = spawn(move || {
        loop {
            // get gyro informatione
            // get stabilisation values
            // refresh motor state + command state
            // reset command state
        }
    });

    sender.join().expect("Flight Thread paniced!")
}
