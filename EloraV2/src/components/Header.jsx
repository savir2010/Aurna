import React, { useState, useEffect } from "react";
import { getFirestore, doc, getDoc } from "firebase/firestore";
import { getAuth, signOut } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import logo from '../assets/logo.png';
import app from "../../firebaseConfig";

const Header = ({ onMicPress, micAnimation }) => {
  const db = getFirestore(app);
  const auth = getAuth(app);
  const navigate = useNavigate();

  const [role, setRole] = useState("");
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(async (user) => {
      if (user) {
        const docRef = doc(db, "users", user.uid);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
          setRole(docSnap.data().role);
          setUser({
            uid: user.uid,
            email: user.email,
            name: docSnap.data().name, // Get user's name from Firestore
          });
        } else {
          setUser({
            uid: user.uid,
            email: user.email,
            name: "User", // Fallback if name isn't in Firestore
          });
        }
      } else {
        setUser(null);
        setRole("");
      }
    });

    return () => unsubscribe();
  }, [auth, db]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate("/");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <>
      <style>
        {`
          @keyframes pulse {
            0% {
              transform: scale(1);
            }
            50% {
              transform: scale(1.1);
            }
            100% {
              transform: scale(1);
            }
          }

          .mic-animation {
            animation: pulse 0.5s ease-in-out;
          }
        `}
      </style>
      <header className="flex items-center justify-between p-4 bg-white text-white">
        <div className="flex items-center space-x-4">
          <a href="/">
            <img className="cursor-pointer w-24 ml-4" src={logo} alt="Logo" />
          </a>
          {role && <span className="text-black mt-3 font-medium">{role}</span>}
        </div>

        <div className="flex items-center space-x-4">
          <div className="relative">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className={`w-6 h-6 cursor-pointer hover:shadow-lg ${
                micAnimation ? "mic-animation" : ""
              }`}
              viewBox="0 0 384 512"
              onClick={onMicPress}
            >
              <path d="M192 0C139 0 96 43 96 96l0 160c0 53 43 96 96 96s96-43 96-96l0-160c0-53-43-96-96-96zM64 216c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 89.1 66.2 162.7 152 174.4l0 33.6-48 0c-13.3 0-24 10.7-24 24s10.7 24 24 24l72 0 72 0c13.3 0 24-10.7 24-24s-10.7-24-24-24l-48 0 0-33.6c85.8-11.7 152-85.3 152-174.4l0-40c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 70.7-57.3 128-128 128s-128-57.3-128-128l0-40z" />
            </svg>
          </div>
          {user && (
            <>
              <button
                onClick={handleLogout}
                className="bg-red-500 text-white px-4 py-2 rounded hover:shadow-lg"
              >
                Logout
              </button>
              <div className="flex items-center space-x-2">
                <span className="text-black font-medium ml-2 mr-3 hover:underline">
                  {user.name}
                </span>
                <img
                  src="https://media.licdn.com/dms/image/v2/D5635AQGCjPEKUZaewg/profile-framedphoto-shrink_800_800/profile-framedphoto-shrink_800_800/0/1737182305628?e=1741478400&v=beta&t=jCpKL85fTdzMlipZ7h-A1PNMK5g4rraZnz8lGtAxPtc"
                  alt="Profile"
                  className="w-10 h-10 rounded-full"
                />
              </div>
            </>
          )}
        </div>
      </header>
    </>
  );
};

export default Header;