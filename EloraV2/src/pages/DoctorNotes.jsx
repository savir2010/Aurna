import React, { useState, useEffect } from "react";
import { db, auth } from "../../firebaseConfig";
import { doc, getDoc, setDoc, updateDoc } from "firebase/firestore";

function DoctorNotes({ selectedPatient }) {
  const [doctorNotes, setDoctorNotes] = useState("");
  const user = auth.currentUser; // Get logged-in doctor

  useEffect(() => {
    if (selectedPatient) {
      fetchDoctorNotes(selectedPatient);
    }
  }, [selectedPatient]);

  const fetchDoctorNotes = async (patientId) => {
    if (!user) return;

    try {
      const docRef = doc(db, "users", user.uid, "patients", patientId);
      const docSnap = await getDoc(docRef);

      if (docSnap.exists()) {
        setDoctorNotes(docSnap.data().doctorNotes || "");
      } else {
        console.log("No notes found for this patient.");
      }
    } catch (error) {
      console.error("Error fetching notes:", error);
    }
  };

  const saveDoctorNotes = async () => {
    if (!user || !selectedPatient) return;

    try {
      const docRef = doc(db, "users", user.uid, "patients", selectedPatient);
      await setDoc(docRef, { doctorNotes }, { merge: true });

      alert("Notes saved successfully!");
    } catch (error) {
      console.error("Error saving notes:", error);
    }
  };

  return (
    <div className="rightside bg-white rounded-xl shadow-md flex flex-col items-start justify-start h-half w-full p-6 mb-4">
      <h1 className="font-extrabold mt-6">Doctor's Notes</h1>
      <textarea
        className="w-full h-40 p-3 mt-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Write notes about the patient here..."
        value={doctorNotes}
        onChange={(e) => setDoctorNotes(e.target.value)}
      />
      <button 
        className="mt-3 bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-600 transition"
        onClick={saveDoctorNotes}
      >
        Save Notes
      </button>
    </div>
  );
}

export default DoctorNotes;
