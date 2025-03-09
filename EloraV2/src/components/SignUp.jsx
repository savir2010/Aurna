import React from "react";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import { getFirestore, doc, setDoc } from "firebase/firestore";
import app from "../../firebaseConfig";

function SignUp() {
  const auth = getAuth(app);
  const db = getFirestore(app);
  const navigate = useNavigate();
  const provider = new GoogleAuthProvider();

  const signInWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      // Create/Update user data in Firestore
      await setDoc(doc(db, "users", user.uid), {
        email: user.email,
        name: user.displayName,
        role: "doctor",
        uid: user.uid,
        doctorNotes: "",
        createdAt: new Date(),
      });

      console.log("Doctor signed in and saved:", user);
      navigate("/dashboard");
    } catch (error) {
      console.error("Error signing in with Google:", error.message);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.heading}>Sign Up</h1>
        <p style={styles.subText}>Sign up as a doctor to continue:</p>
        <input type="email" placeholder="Email" style={styles.input} />
        <input type="password" placeholder="Password" style={styles.input} />
        <button onClick={signInWithGoogle} style={styles.googleButton}>
          Sign Up as Doctor
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    margin: 0,
    background: "#f7f7f7",
  },
  card: {
    background: "#fff",
    padding: "2rem",
    borderRadius: "8px",
    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
    textAlign: "center",
    maxWidth: "350px",
    width: "100%",
  },
  heading: {
    margin: "0 0 1rem",
    fontSize: "1.8rem",
    fontWeight: 600,
  },
  subText: {
    margin: "0 0 2rem",
    color: "#555",
  },
  googleButton: {
    background: "#4285F4",
    color: "#fff",
    padding: "0.8rem 1.5rem",
    border: "none",
    borderRadius: "5px",
    fontSize: "1rem",
    cursor: "pointer",
  },
  input: {
    width: "100%",
    padding: "0.8rem",
    marginBottom: "1rem",
    border: "1px solid #ddd",
    borderRadius: "5px",
  },
  input: {
    width: "100%",
    padding: "0.8rem",
    margin: "0.5rem 0",
    border: "1px solid #ddd",
    borderRadius: "5px",
    fontSize: "1rem",
    marginBottom: "1rem"
  },
};

export default SignUp;
