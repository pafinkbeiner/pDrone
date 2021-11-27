const rpio = require("rpio");

class PWM {

    constructor(pin, freq) {
        this.pin = pin;
        this.freq = freq;
        this.duty = 0;
        this.running = false;
        this.setup();
    }

    setup() {
        rpio.open(this.pin, rpio.PWM);
        rpio.pwmSetClockDivider(rpio.PWM_CLOCK_DIVIDER_32);
        rpio.pwmSetRange(this.pin, 100);
        rpio.pwmSetMode(this.pin, rpio.PWM_MODE_MS);
    }

    start() {
        this.running = true;
        rpio.pwmSetData(this.pin, this.duty);
    }

    stop() {
        this.running = false;
        rpio.pwmSetData(this.pin, 0);
    }

    setDuty(duty) {
        this.duty = duty;
        if (this.running) {
            rpio.pwmSetData(this.pin, this.duty);
        }
    }

    setFreq(freq) {
        this.freq = freq;
        if (this.running) {
            rpio.pwmSetClockDivider(rpio.PWM_CLOCK_DIVIDER_32);
            rpio.pwmSetRange(this.pin, 100);
            rpio.pwmSetMode(this.pin, rpio.PWM_MODE_MS);
            rpio.pwmSetData(this.pin, this.duty);
        }
    }

}

module.exports = PWM;