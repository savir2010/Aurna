import React, { useState, useEffect } from "react";
import Header from "../components/Header";
import DonutChart from "../components/DonutChart";
import LineGraph from "../components/LineGraph";
import eeg_sensors from '../assets/eeg_sensors.mp4';
import eeg_waves from '../assets/eeg_waves.mp4';
import { onAuthStateChanged } from "firebase/auth";
import { db, auth } from "../../firebaseConfig";
import { collection, getDocs, setDoc, doc } from "firebase/firestore";
import DoctorNotes from "./DoctorNotes";
import { jsPDF } from "jspdf"; // For generating PDFs

function DoctorDashboard() {
  const [micPressed, setMicPressed] = useState(false);
  const [videoPlaying, setVideoPlaying] = useState(false);
  const [micAnimation, setMicAnimation] = useState(false); // State for mic animation

  const [stressScore, setStressScore] = useState(50);
  const [imageUrl, setImageUrl] = useState('');
  const [labels, setLabels] = useState('');
  const [report, setReport] = useState('No report found yet');
  const [prediction, setPrediction] = useState('No prediction found yet');

  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [user, setUser] = useState(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [scanType, setScanType] = useState('');
  const [scanResult, setScanResult] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        setUser(currentUser);
        fetchPatients(currentUser.uid);  // Fetch patients after auth is ready
      }
    });
    return () => unsubscribe();  // Cleanup listener on unmount
  }, []);

  const fetchPatients = async (doctorId) => {
    if (!doctorId) return;
  
    try {
      const patientsRef = collection(db, "users", doctorId, "patients");
      const querySnapshot = await getDocs(patientsRef);
  
      if (querySnapshot.empty) {
        console.log("No patients found. Creating demo patients...");
  
        // Create demo patients
        await setDoc(doc(patientsRef, "patient1"), {
          name: "Patient 1",
          doctorNotes: "Initial Notes for Patient 1",
          anxietyScores: [50, 60, 70] // Mock data
        });
  
        await setDoc(doc(patientsRef, "patient2"), {
          name: "Patient 2",
          doctorNotes: "Initial Notes for Patient 2",
          anxietyScores: [40, 55, 65] // Mock data
        });
  
        console.log("Demo patients created!");
      }
  
      // Fetch updated patient list after creation
      const updatedSnapshot = await getDocs(patientsRef);
      const patientList = updatedSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setPatients(patientList);
    } catch (error) {
      console.error("Error fetching patients:", error);
    }
  };

  const fetchPrediction = async () => {
    const controller = new AbortController();
    const timeout = setTimeout(() => {
      controller.abort();
    },140000); // Timeout set to 10 seconds
  
    try {
      const response = await fetch("http://127.0.0.1:5000/record_predict", {
        method: "POST",
        signal: controller.signal,
      });
      clearTimeout(timeout);
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      setLabels(data.labels);
      setStressScore((data.stress_score * 100).toFixed(2));
      setImageUrl(data.image_url);
      setReport(data.report);
      setPrediction(data.prediction);
    } catch (error) {
      if (error.name === 'AbortError') {
        console.error("Request timed out:", error);
        alert("EEG prediction request timed out.");
      } else {
        console.error("Error fetching prediction:", error);
        alert("Failed to fetch EEG prediction.");
      }
    }
  };

  const handleMicPress = () => {
    setMicPressed(true);
    setVideoPlaying(true); // Start playing videos
    setMicAnimation(true); // Trigger animation

    // Reset animation after it completes
    setTimeout(() => {
      setMicAnimation(false);
    }, 500); // Match the duration of the animation

    fetchPrediction();
  };

  const handleFileUpload = (file) => {
    setSelectedFile(file);
  };

  const handleScanUpload = async () => {
    if (!selectedFile || !scanType) {
      alert("Please select a file and scan type first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const endpoint = scanType === "mri" 
        ? "http://127.0.0.1:5000/predict_mri_brain_tumor" 
        : "http://127.0.0.1:5000/predict_lung_cancer";

      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setScanResult(data);
    } catch (error) {
      console.error("Error uploading scan:", error);
      alert("Failed to upload scan.");
    }
  };

  const downloadReport = () => {
    const doc = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "a4",
    });
  
    const marginLeft = 20; // Left margin
    const marginTop = 20;  // Top margin
    const lineHeight = 10; // Space between lines
  
    let y = marginTop; // Start from the top margin
  
    doc.setFontSize(12);
    doc.text("Patient Report", marginLeft, y);
    y += lineHeight;
  
    doc.text(`Stress Score: ${stressScore}%`, marginLeft, y);
    y += lineHeight;
  
    doc.text(`Prediction: ${prediction}`, marginLeft, y);
    y += lineHeight;
  
    doc.text(`Report: ${report}`, marginLeft, y);
    y += lineHeight;
  
    if (scanResult) {
      doc.text(`Scan Result - Predicted Class: ${scanResult["Predicted Class"]}`, marginLeft, y);
      y += lineHeight;
      
      doc.text(`Confidence: ${scanResult["Confidence"]}`, marginLeft, y);
      y += lineHeight;
    }
  
    doc.save("patient_report.pdf");
  };
  

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header onMicPress={handleMicPress} micAnimation={micAnimation} />
      <main className="p-6 grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="container flex flex-row w-[100vw] space-x-6 ml-20">
          <div className="leftside flex flex-col space-y-6 w-3/4">
            <div className="row-1 flex space-x-3">
              <div className="bg-white p-6 rounded-xl shadow-md flex flex-col items-center justify-center h-40 w-48">
                <h1 className="font-bold">Stressed?</h1>
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
                <h1 className="font-bold">How you feeling?</h1>
                <h1>{labels}, {prediction}</h1>
              </div>
            </div>

            {/* Brainwaves Video */}
            <div className="bg-white p-6 rounded-xl shadow-md w-full relative flex flex-col items-center justify-center">
              <h1 className="font-extrabold mb-2">Brainwaves</h1>
              {videoPlaying ? (
                <video width="640" height="360" loop muted autoPlay preload="auto">
                  <source src={eeg_waves} type="video/mp4" />
                </video>
              ) : (
                <div className="w-full h-auto bg-gray-900 flex flex-col items-center justify-center rounded-lg relative">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="white"
                    className="w-20 h-20 cursor-pointer opacity-80 hover:opacity-100 transition"
                  >
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </div>
              )}
            </div>

            {/* Neural Sensors Video */}
            <div className="bg-white p-6 rounded-xl shadow-md w-full relative flex flex-col items-center justify-center">
              <h1 className="font-extrabold mb-2">Neural Sensors</h1>
              {videoPlaying ? (
                <video width="640" height="360" loop muted autoPlay preload="auto">
                  <source src={eeg_sensors} type="video/mp4" />
                </video>
              ) : (
                <div className="w-full h-auto bg-gray-900 flex flex-col items-center justify-center rounded-lg relative">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="white"
                    className="w-20 h-20 cursor-pointer opacity-80 hover:opacity-100 transition"
                  >
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </div>
              )}
            </div>

            {/* Past Anxiety Score History */}
            <div className="bg-white p-6 rounded-xl shadow-md w-full">
              <h1 className="font-extrabold">Anxiety Score History</h1>
              <LineGraph />
            </div>

            {/* Upload Scan Section */}
            <div className="bg-white p-6 rounded-xl shadow-md w-full">
              <h1 className="font-extrabold mb-4">Upload Scan</h1>
              <select
                className="w-full p-2 mt-2 border rounded"
                onChange={(e) => setScanType(e.target.value)}
                value={scanType}
              >
                <option value="">Select Scan Type</option>
                <option value="mri">MRI Scan</option>
                <option value="ct">CT Scan</option>
              </select>
              <input
                type="file"
                accept=".jpg, .jpeg, .png" // Accept common image formats
                onChange={(e) => handleFileUpload(e.target.files[0])}
                className="w-full p-2 mt-2 border rounded"
              />
              <button
                onClick={handleScanUpload}
                className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
                disabled={!selectedFile || !scanType}
              >
                Upload Scan
              </button>
            </div>

            {/* Scan Results Section */}
            <div className="bg-white p-6 rounded-xl shadow-md w-full mt-6">
              <h1 className="font-extrabold mb-4">Scan Results</h1>
              {scanResult ? (
                <div className="p-4 border border-gray-300 rounded-lg bg-gray-50">
                  <p className="text-gray-700 text-lg leading-relaxed font-medium">
                    <strong>Predicted Class:</strong> {scanResult["Predicted Class"]}
                  </p>
                  <p className="text-gray-700 text-lg leading-relaxed font-medium">
                    <strong>Confidence:</strong> {scanResult["Confidence"]}
                  </p>
                </div>
              ) : (
                <p className="text-gray-700 text-lg leading-relaxed font-medium">
                  No scan results available.
                </p>
              )}
            </div>
          </div>

          {/* Right side */}
          <div className="rightside bg-white rounded-xl shadow-md flex flex-col items-start justify-start h-full w-full p-6">
            {/* Doctor's Notes */}
            <div className="container">
              <h1 className="font-extrabold mb-4"> Select Patient </h1>
              <select
                className="w-full p-2 mt-2 border rounded"
                onChange={(e) => setSelectedPatient(e.target.value)}
                value={selectedPatient}
              >
                <option value="">Select a patient</option>
                {patients.map((patient) => (
                  <option key={patient.id} value={patient.id}>{patient.name}</option>
                ))}
              </select>

              {selectedPatient && <DoctorNotes selectedPatient={selectedPatient} />}
             </div>

            {/* Report Section */}
            <h1 className="font-extrabold mb-4"> Report </h1>
            <div className="max-h-64 w-full overflow-y-auto p-4 border border-gray-300 rounded-lg bg-gray-50">
              <p className="text-gray-700 text-lg leading-relaxed font-medium">{report}</p>
            </div>
            <button
              onClick={downloadReport}
              className="bg-green-500 text-white px-4 py-2 rounded mt-4"
            >
              Download Report
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default DoctorDashboard;