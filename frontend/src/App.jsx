import { useState } from 'react'
import './App.css'
import HeartForm from './HeartForm'

function App() {
  return (
    <div className="fixed top-0 left-0 w-screen h-screen p-0 flex flex-col justify-center items-center"
        style={{
          backgroundImage: "url('/pic3.jpg')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
    >
      <div>
        <h1 className='p-1 m-1 text-3xl text-black'>HEART DISEASE PREDICTION</h1>
      </div>
      <div
        className="h-[100%] bg-cover overflow-auto"
      >
        <HeartForm />
      </div>
      
    </div>
  );
}


export default App
