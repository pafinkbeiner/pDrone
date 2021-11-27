import React from 'react';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';

const URL = "http://localhost:8080"

function App() {
  return (
    <div className="App">
      <h1>pSender</h1>

      <div style={{backgroundColor: "red", borderRadius: "6px", padding: "1rem"}} className="vl">
        <h2>VL</h2>
        <button onClick={() => {axios.get(`${URL}/command/vl/5`)}} style={{height: "3rem", width: "6rem"}}>+</button>
        <button onClick={() => {axios.get(`${URL}/command/vl/-5`)}} style={{height: "3rem", width: "6rem"}}>-</button>
      </div>
      <br/>
      <div style={{backgroundColor: "blue", borderRadius: "6px", padding: "1rem"}} className="hl">
        <h2>HL</h2>
        <button onClick={() => {axios.get(`${URL}/command/hl/5`)}} style={{height: "3rem", width: "6rem"}}>+</button>
        <button onClick={() => {axios.get(`${URL}/command/hl/-5`)}} style={{height: "3rem", width: "6rem"}}>-</button>
      </div>
      <br/>
      <div style={{backgroundColor: "green", borderRadius: "6px", padding: "1rem"}} className="vr">
        <h2>VR</h2>
        <button onClick={() => {axios.get(`${URL}/command/vr/5`)}} style={{height: "3rem", width: "6rem"}}>+</button>
        <button onClick={() => {axios.get(`${URL}/command/vr/-5`)}} style={{height: "3rem", width: "6rem"}}>-</button>
      </div>
      <br/>
      <div style={{backgroundColor: "yellow", borderRadius: "6px", padding: "1rem"}} className="hr">
        <h2>HR</h2>
        <button onClick={() => {axios.get(`${URL}/command/hr/5`)}} style={{height: "3rem", width: "6rem"}}>+</button>
        <button onClick={() => {axios.get(`${URL}/command/hr/-5`)}} style={{height: "3rem", width: "6rem"}}>-</button>
      </div>

    </div>
  );
}

export default App;
