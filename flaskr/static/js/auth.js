import { auth, googleProvider } from "./firebase-config.js";
import { createUserWithEmailAndPassword, sendEmailVerification, signInWithEmailAndPassword, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";

console.log("auth.js loaded successfully!");

// Register function
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const username = document.getElementById('register-username').value;

    try {
        // Create user with email and password
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const idToken = await userCredential.user.getIdToken();
        const user = userCredential.user;

        // Send email verification
        await sendEmailVerification(user);
        alert("A verification email has been sent to your email address. Please verify your email to complete registration.");

        // Send ID token and username to backend for registration
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ idToken, username, email }),
        });

        const data = await response.json();
        if (data.success) {
            alert('Registration successful! Please login.');
            window.location.href = '/login'; // Redirect to login page
        } else {
            alert('Registration failed!');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Registration failed!');
    }
});

// Login function
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    console.log("Attempting to log in with:", email, password);

    try {
        // Sign in with email and password
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        //console.log("User signed in successfully:", userCredential.user);

        // Check if email is verified
        if (!user.emailVerified) {
            alert("Please verify your email before logging in.");
            return;
        }

        // Get the ID token
        const idToken = await user.getIdToken();
        //console.log("ID token:", idToken);

        // Send ID token to backend for verification
        const response = await fetch('/verify_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ idToken }),
        });

        const data = await response.json();
        //console.log("Backend response:", data);

        if (data.success) {
            window.location.href = '/dashboard'; // Redirect to cpanel
        } else {
            alert('Login failed!');
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('Login failed!');
    }
});

// Resend verification email
document.getElementById('resend-verification-link').addEventListener('click', async (e) => {
    e.preventDefault();

    const user = auth.currentUser;
    if (!user) {
        alert("Please log in first.");
        return;
    }

    try {
        await sendEmailVerification(user);
        alert("A new verification email has been sent to your email address.");
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to resend verification email.');
    }
});

// Google Sign-In function
document.getElementById('google-sign-in-button').addEventListener('click', async () => {
    try {
        // Sign in with Google
        const result = await signInWithPopup(auth, googleProvider);
        const user = result.user;

        // Get the ID token
        const idToken = await user.getIdToken();

        // Send ID token to backend for verification
        const response = await fetch('/verify_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ idToken }),
        });

        const data = await response.json();
        if (data.success) {
            window.location.href = '/cpanel'; // Redirect to cpanel
        } else {
            alert('Login failed!');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Google Sign-In failed!');
    }
});


