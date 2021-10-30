
async function update_telemetry() {
    
    var gyro_xyz = {x: 4, y: 5, z: 6};
    var accel_xyz = { x: 7, y: 8, z: 9 };
    
    var gyro_data = {
        gyro_xyz: gyro_xyz,
        accel_xyz: accel_xyz,
        rollpitch: { roll: 10, pitch: 11 }
    }
    
    console.log(gyro_data);
}

module.exports = update_telemetry;