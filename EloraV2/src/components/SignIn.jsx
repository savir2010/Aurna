import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import app from "../../firebaseConfig";

function SignIn() {
  const auth = getAuth(app);
  const navigate = useNavigate();
  const provider = new GoogleAuthProvider();

  const signInWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      console.log("User signed in:", user);
      navigate("/dashboard");
    } catch (error) {
      console.error("Error signing in with Google:", error.message);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "2rem" }}>
      <h1>Sign In</h1>
      <p>Sign in with your Google account to continue:</p>

      <button 
        onClick={signInWithGoogle}
        style={{ background: "#4285F4", color: "white", padding: "10px 20px", border: "none", borderRadius: "5px", fontSize: "16px", cursor: "pointer" }}
      >
        Sign In with Google
      </button>
    </div>
  );
}

export default SignIn;
