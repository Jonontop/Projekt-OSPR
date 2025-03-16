// Toggle between login and register forms
document.getElementById('show-register-link').addEventListener('click', (e) => {
    e.preventDefault();
    document.querySelector('.login-form').style.display = 'none';
    document.querySelector('.register-form').style.display = 'block';
});

document.getElementById('show-login-link').addEventListener('click', (e) => {
    e.preventDefault();
    document.querySelector('.register-form').style.display = 'none';
    document.querySelector('.login-form').style.display = 'block';
});