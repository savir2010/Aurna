import { initializeApp, getApps } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";


const firebaseConfig = {
  apiKey: "AIzaSyB7zQT-Bt5BNpVFxD3QdsQqbSr_xGuSM3U",
  authDomain: "elora-97f63.firebaseapp.com",
  projectId: "elora-97f63",
  storageBucket: "elora-97f63.firebasestorage.app",
  messagingSenderId: "440695011113",
  appId: "1:440695011113:web:8543735a2b034c8708e938"
};

const app = getApps().length ? getApps()[0] : initializeApp(firebaseConfig);

export default app;
export const auth = getAuth(app);
export const db = getFirestore(app);