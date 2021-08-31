import React from 'react';
import logo from './logo.svg';
import { io } from "socket.io-client";
import './App.css';

// const socket = io("http://localhost:8080", {  transports: ["websocket"] });
export const socket = io("http://localhost:8080");

socket.on("connect", () => {
  console.log("Connected to the server");
});

socket.on("disconnect", () => {
  console.log("Disconected from the server");
});

function App() {
  return (
    <div className="App">
      <h1>pSender</h1>

      <div style={{backgroundColor: "red", borderRadius: "6px", padding: "1rem"}} className="vl">
        <h2>VL</h2>
        <button onClick={() => socket.emit("command", JSON.stringify({ 'vl': 5, 'vr': 0, 'hl': 0, 'hr': 0 }))} style={{height: "3rem", width: "6rem"}}>+</button>
        <button onClick={() => socket.emit("command", JSON.stringify({ 'vl': -5, 'vr': 0, 'hl': 0, 'hr': 0 }))} style={{height: "3rem", width: "6rem"}}>-</button>
      </div>
      <br/>
      <div style={{backgroundColor: "blue", borderRadius: "6px", padding: "1rem"}} className="hl">
        <h2>HL</h2>
        <button onClick={() => socket.emit("command", JSON.stringify({ 'vl': 0, 'vr': 0, 'hl': 5, 'hr': 0 }))} style={{height: "3rem", width: "6rem"}}>+</button>
        <button onClick={() => socket.emit("command", JSON.stringify({ 'vl': 0, 'vr': 0, 'hl': -5, 'hr': 0 }))} style={{height: "3rem", width: "6rem"}}>-</button>
      </div>
      <br/>
      <div style={{backgroundColor: "green", borderRadius: "6px", padding: "1rem"}} className="vr">
        <h2>VR</h2>
        <button onClick={() => socket.emit("command", JSON.stringify({ 'vl': 0, 'vr': 5, 'hl': 0, 'hr': 0 }))} style={{height: "3rem", width: "6rem"}}>+</button>
        <button onClick={() => socket.emit("command", JSON.stringify({ 'vl': 0, 'vr': -5, 'hl': 0, 'hr': 0 }))} style={{height: "3rem", width: "6rem"}}>-</button>
      </div>
      <br/>
      <div style={{backgroundColor: "yellow", borderRadius: "6px", padding: "1rem"}} className="hr">
        <h2>HR</h2>
        <button onClick={() => socket.emit("command", JSON.stringify({ 'vl': 0, 'vr': 0, 'hl': 0, 'hr': 5 }))} style={{height: "3rem", width: "6rem"}}>+</button>
        <button onClick={() => socket.emit("command", JSON.stringify({ 'vl': 0, 'vr': 0, 'hl': 0, 'hr': -5 }))} style={{height: "3rem", width: "6rem"}}>-</button>
      </div>

    </div>
  );
}

export default App;
