document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('access_token')) {
        window.location.href = '/game/';
    }

    const loginForm = document.getElementById('login-form');

    async function login(username, password) {
        try {
            const response = await fetch('/token/token/get/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                console.log('Удачный вход!');
                window.location.href = '/game/';
            } else {
                console.error('Ошибка входа:', response.statusText);
                alert('Ошибка входа. Проверьте свои данные.');
            }
        } catch (error) {
            console.error('Ошибка при входе в систему:', error);
        }
    }

    // Обработчик отправки формы
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        login(username, password);
    });
});