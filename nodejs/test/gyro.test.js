
async function update_telemetry() {
    
    var gyro_data = { gyro_xyz: { x: 112, y: 240, z: -472 },
    accel_xyz: { x: -288, y: 1156, z: 15744 },                                                                                                                                                                                                 
    rollpitch: { roll: 1.7578125, pitch: -7.0556640625 } }
    
    return gyro_data;
}

module.exports = update_telemetry;