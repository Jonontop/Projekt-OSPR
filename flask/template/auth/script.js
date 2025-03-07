// Toggle between Login and Register Forms
const showRegisterLink = document.getElementById("show-register-link");
const showLoginLink = document.getElementById("show-login-link");

const loginForm = document.querySelector(".login-form");
const registerForm = document.querySelector(".register-form");

showRegisterLink.addEventListener("click", (e) => {
  e.preventDefault();
  loginForm.style.display = "none";
  registerForm.style.display = "block";
});

showLoginLink.addEventListener("click", (e) => {
  e.preventDefault();
  registerForm.style.display = "none";
  loginForm.style.display = "block";
});
