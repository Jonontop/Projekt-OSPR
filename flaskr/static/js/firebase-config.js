import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

//web app's Firebase configuration
// Nism biu dost sposoben dt tega v posebi .env
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
const app = initializeApp(firebaseConfig); // Initialize Firebase
const auth = getAuth(app); // Get the Auth service for the default app
const googleProvider = new GoogleAuthProvider(); // Create a new instance of the Google provider object

//export { auth, db, googleProvider };
export { auth, googleProvider };

// Export auth for use in other modules
 window.auth = auth;



