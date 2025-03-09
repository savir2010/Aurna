import Header from "./components/Header";
import DonutChart from "./components/DonutChart";
import LineGraph from "./components/LineGraph";
import eeg_sensors from './assets/eeg_sensors.mp4'
import eeg_waves from './assets/eeg_waves.mp4'
import React, { useState, useEffect } from "react";

function App() {
  const [micPressed, setMicPressed] = useState(false);
  const [stressScore, setStressScore] = useState(50);
  const [imageUrl, setImageUrl] = useState('');
  const [labels, setLabels] = useState('');
  const [report, setReport] = useState('No report found yet');
  const [doctorNotes, setDoctorNotes] = useState(localStorage.getItem("doctorNotes") || "");

  useEffect(() => {
    localStorage.setItem("doctorNotes", doctorNotes);
  }, [doctorNotes]);

  const fetchPrediction = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/record_predict", {
        method: "POST"
      });
      const data = await response.json();

      setLabels(data.labels);
      setStressScore((data.stress_score * 100).toFixed(2));
      setImageUrl(data.image_url);
      setReport(data.report);
      console.log(data.labels);
      console.log(data.image_url);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      alert("Failed to fetch EEG prediction.");
    }
  };

  const handleMicPress = () => {
    setMicPressed(true);
    fetchPrediction();
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header onMicPress={() => setMicPressed(true)} />
      <main className="p-6 grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="container flex flex-row w-[100vw] space-x-6 ml-20">
          {/* Left side */}
          <div className="leftside flex flex-col space-y-6 w-3/4">
            <div className="row-1 flex space-x-3">
              <div className="bg-white p-6 rounded-xl shadow-md flex items-center justify-center h-40 w-48">
                <DonutChart percentage={stressScore} />
              </div>
              <div 
                className={`bg-white p-6 rounded-xl shadow-md flex items-center justify-center h-40 w-64`} 
                style={{
                  backgroundImage: micPressed ? `url(${imageUrl})` : 'none', 
                  backgroundSize: 'cover', 
                  backgroundPosition: 'center'
                }}
              />
              <div className="bg-white p-6 rounded-xl shadow-md flex-col items-center justify-center h-40 w-48">
                <h1 className="font-bold">Current Mood</h1>
                <h1>{labels}</h1>
              </div>
            </div>
            <div className="row-2 flex">
              <div className="bg-white p-6 rounded-xl shadow-md w-full">
                <h1 className="font-extrabold">Brainwaves</h1>
                <video width="640" height="360" loop muted autoPlay preload="auto">
                  <source src={eeg_waves} type="video/mp4"/>
                </video>
              </div>
            </div>
            <div className="row3 flex">
              <div className="bg-white p-6 rounded-xl shadow-md w-full">
                <h1 className="font-extrabold">Neural Sensors</h1>
                <video width="640" height="360" loop muted autoPlay preload="auto">
                  <source src={eeg_sensors} type="video/mp4"/>
                </video>
              </div>
            </div>
            <div className="row4 flex">
              <div className="bg-white p-6 rounded-xl shadow-md w-full">
                <h1 className="font-extrabold">History</h1>
                <LineGraph />
              </div>
            </div>
          </div>

          {/* Right side */}
          <div className="rightside bg-white rounded-xl shadow-md flex flex-col items-start justify-start h-full w-full p-6">
            <h1 className="font-extrabold mb-4"> Report </h1>
            <div className="max-h-64 w-full overflow-y-auto p-4 border border-gray-300 rounded-lg bg-gray-50">
              <p className="text-gray-700 text-lg leading-relaxed font-medium">{report}</p>
            </div>

            {/* Doctor Notes Box */}
            <h1 className="font-extrabold mt-6">Doctor's Notes</h1>
            <textarea
              className="w-full h-40 p-3 mt-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Write notes about the patient here..."
              value={doctorNotes}
              onChange={(e) => setDoctorNotes(e.target.value)}
            />
            <button 
              className="mt-3 bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-600 transition"
              onClick={() => localStorage.setItem("doctorNotes", doctorNotes)}
            >
              Save Notes
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
