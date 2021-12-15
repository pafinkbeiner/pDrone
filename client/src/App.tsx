import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';

const URL = "http://10.0.0.4:8080"

function App() {

  const [motor, setMotor] = useState()

  useEffect(() => {

    // setInterval(() => {

    // }, 1000)

  }, [])

  const refreshMotor = () => {
    axios.get(`${URL}/motor`).then(res => {
      setMotor(res.data)
    })
  }

  return (
    <div className="App">
      <h1>pSender</h1>

      {
        motor && <>{JSON.stringify(motor)}</>
      }

      <br/><br/>

      <button onClick={() => {
        axios.get(`${URL}/flight/1`)

      }} style={{ height: "3rem", width: "6rem" }}>Flight ON</button>
      <button onClick={() => {
        axios.get(`${URL}/flight/0`)

      }} style={{ height: "3rem", width: "6rem" }}>FLight OFF</button>

      <br/><br/>

      <div style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
        <div style={{ display: "flex", flexDirection: "row" }}>

          <div style={{ backgroundColor: "red", borderRadius: "6px", padding: "1rem" }} className="vl">
            <h2>VL</h2>
            <button onClick={() => { axios.get(`${URL}/command/vl/5`) }} style={{ height: "3rem", width: "6rem" }}>+</button>
            <button onClick={() => { axios.get(`${URL}/command/vl/-5`) }} style={{ height: "3rem", width: "6rem" }}>-</button>
          </div>

          <div style={{ backgroundColor: "green", borderRadius: "6px", padding: "1rem" }} className="vr">
            <h2>VR</h2>
            <button onClick={() => { axios.get(`${URL}/command/vr/5`) }} style={{ height: "3rem", width: "6rem" }}>+</button>
            <button onClick={() => { axios.get(`${URL}/command/vr/-5`) }} style={{ height: "3rem", width: "6rem" }}>-</button>
          </div>

        </div>

        <div style={{ display: "flex", flexDirection: "row" }}>

          <div style={{ backgroundColor: "blue", borderRadius: "6px", padding: "1rem" }} className="hl">
            <h2>HL</h2>
            <button onClick={() => { axios.get(`${URL}/command/hl/5`) }} style={{ height: "3rem", width: "6rem" }}>+</button>
            <button onClick={() => { axios.get(`${URL}/command/hl/-5`) }} style={{ height: "3rem", width: "6rem" }}>-</button>
          </div>

          <div style={{ backgroundColor: "yellow", borderRadius: "6px", padding: "1rem" }} className="hr">
            <h2>HR</h2>
            <button onClick={() => { axios.get(`${URL}/command/hr/5`) }} style={{ height: "3rem", width: "6rem" }}>+</button>
            <button onClick={() => { axios.get(`${URL}/command/hr/-5`) }} style={{ height: "3rem", width: "6rem" }}>-</button>
          </div>

        </div>
      </div>

      <br/>
      <br/>

      <div style={{ backgroundColor: "orange", borderRadius: "6px", padding: "1rem" }} className="hr">
        <h2>ALL</h2>
        <button onClick={() => {
          axios.get(`${URL}/command/hr/5`).then(() => {
            axios.get(`${URL}/command/hl/5`).then(() => {
              axios.get(`${URL}/command/vr/5`).then(() => {
                axios.get(`${URL}/command/vl/5`).then(() => {
                  refreshMotor()
                })
              })
            })
          })
        }} style={{ height: "3rem", width: "6rem" }}>+</button>
        <button onClick={() => {
          axios.get(`${URL}/command/hr/-5`).then(() => {
            axios.get(`${URL}/command/hl/-5`).then(() => {
              axios.get(`${URL}/command/vr/-5`).then(() => {
                axios.get(`${URL}/command/vl/-5`).then(() => {
                  refreshMotor()
                })
              })
            })
          })
        }} style={{ height: "3rem", width: "6rem" }}>-</button>
      </div>



    </div>
  );
}

export default App;
