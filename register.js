// API URL (Replace with the actual API URL)
const API_BASE_URL = 'https://api.example.com';

// Registration Form Submission
document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const userData = { name, email, password };

    try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        const data = await response.json();
        console.log('User registered:', data);
        alert('Registration successful!');
    } catch (error) {
        console.error('Error:', error);
        alert('Registration failed.');
    }
});

// Login Form Submission
document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const credentials = { email, password };

    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials)
        });
        const data = await response.json();
        console.log('User logged in:', data);

        // Store token for further API requests
        localStorage.setItem('authToken', data.token);
        alert('Login successful!');
        document.getElementById('counselor-section').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed.');
    }
});

// Mood Tracking Form Submission
document.getElementById('moodForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const mood = document.getElementById('mood').value;
    const thoughts = document.getElementById('thoughts').value;

    const moodData = { mood, thoughts };

    const token = localStorage.getItem('authToken');

    try {
        const response = await fetch(`${API_BASE_URL}/mood`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(moodData)
        });
        const data = await response.json();
        console.log('Mood recorded:', data);
        alert('Mood recorded successfully!');
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to record mood.');
    }
});

// Connect with Counselor
document.getElementById('connectCounselorBtn').addEventListener('click', async function() {
    const token = localStorage.getItem('authToken');

    try {
        const response = await fetch(`${API_BASE_URL}/counselor/connect`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
        console.log('Counselor connected:', data);
        alert('Connected to counselor!');
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to connect to counselor.');
    }
});
