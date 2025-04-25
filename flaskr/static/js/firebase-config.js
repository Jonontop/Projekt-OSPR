import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
require('dotenv').config();


// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: `${process.env.FIREBASE_API_KEY}`,
    authDomain: "ospr-6320a.firebaseapp.com",
    projectId: "ospr-6320a",
    storageBucket: "ospr-6320a.firebasestorage.app",
    messagingSenderId: `${process.env.FIREBASE_MESSAGING_SENDER_ID}`,
    appId: `${process.env.FIREBASE_APP_ID}`,
    measurementId: `${process.env.FIREBASE_MEASUREMENT_ID}`
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig); // Initialize Firebase
const auth = getAuth(app); // Get the Auth service for the default app
const googleProvider = new GoogleAuthProvider(); // Create a new instance of the Google provider object

//export { auth, db, googleProvider };
export { auth, googleProvider };

// Export auth for use in other modules
window.auth = auth;



