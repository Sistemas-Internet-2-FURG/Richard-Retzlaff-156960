document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const formData = {
        username: username,
        password: password
    };

    try {
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token);
            }
            window.location.href = './home.html';
        } else {
            alert('Erro ao realizar o login. Por favor, tente novamente.');
            window.location.reload();
        }
    } catch (error) {
        alert('Erro de conexão. Por favor, tente novamente.');
        window.location.reload();
    }
});
