const mpu = require("mpu6050");

export class MPU6050{
   
    constructor(i2cBus){
        this.i2cBus = i2cBus;
        this.mpu = new mpu(i2cBus);
        this.mpu.initialize();
    }

    getGyro(){
        return this.mpu.getMotion6();
    }
    
}