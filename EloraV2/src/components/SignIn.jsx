import React from "react";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import app from "../../firebaseConfig";

function SignIn() {
  const auth = getAuth(app);
  const navigate = useNavigate();
  const provider = new GoogleAuthProvider();

  const signUpWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      // This will create a new user (or sign them in if they already exist).
      console.log("User signed up with Google:", result.user);
      navigate("/dashboard");
    } catch (error) {
      console.error("Error signing up with Google:", error.message);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.heading}>Sign In</h1>
        <p style={styles.subText}>Join us with your Google account</p>
        <input type="email" placeholder="Email" style={styles.input} />
        <input type="password" placeholder="Password" style={styles.input} />
        <button onClick={signUpWithGoogle} style={styles.googleButton}>
          Sign In with Google
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
    margin: "0.5rem 0",
    border: "1px solid #ddd",
    borderRadius: "5px",
    fontSize: "1rem",
    marginBottom: "1rem"
  },
  input: {
    width: "100%",
    padding: "0.8rem",
    margin: "0.5rem 0",
    border: "1px solid #ddd",
    borderRadius: "5px",
    fontSize: "1rem",
    marginBottom: "1rem",
  }
};

export default SignIn;
