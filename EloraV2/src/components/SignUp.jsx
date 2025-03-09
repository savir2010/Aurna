import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import { getFirestore, doc, setDoc } from "firebase/firestore";
import app from "../../firebaseConfig"; // Ensure this path is correct

function SignUp() {
  const auth = getAuth(app);
  const db = getFirestore(app);
  const navigate = useNavigate();
  const provider = new GoogleAuthProvider();

  const signInWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      // Store doctor information in Firestore
      await setDoc(doc(db, "users", user.uid), {
        email: user.email,
        name: user.displayName,
        role: "doctor",
        uid: user.uid,
        doctorNotes: "",
        createdAt: new Date(),
      });

      console.log("Doctor signed in and saved:", user);
      
      // Navigate to the Doctor Dashboard
      navigate("/dashboard");
    } catch (error) {
      console.error("Error signing in with Google:", error.message);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "2rem" }}>
      <h1>Sign Up</h1>
      <p>Sign up as a doctor to continue:</p>

      <button
        onClick={signInWithGoogle}
        style={{
          background: "#4285F4",
          color: "white",
          padding: "10px 20px",
          border: "none",
          borderRadius: "5px",
          fontSize: "16px",
          cursor: "pointer"
        }}
      >
        Sign Up as Doctor
      </button>
    </div>
  );
}

export default SignUp;
