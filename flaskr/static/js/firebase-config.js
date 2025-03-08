import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth, 
         GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyAjuk6RqUEDLReXaW1vNryZdR2BDRXydKs",
    authDomain: "ospr-6320a.firebaseapp.com",
    projectId: "ospr-6320a",
    storageBucket: "ospr-6320a.firebasestorage.app",
    messagingSenderId: "929635361328",
    appId: "1:929635361328:web:752e995da1ccdfe8bf83f5",
    measurementId: "G-GLB8DD7GTC"
  };

// Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  const provider = new GoogleAuthProvider();
  
  const db = getFirestore(app);
  
  export { auth, provider, db };