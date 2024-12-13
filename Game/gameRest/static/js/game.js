function clearCards() {
    const cardsContainer = document.getElementById('cards');
    cardsContainer.innerHTML = '';
}

document.addEventListener('DOMContentLoaded', () => {
    const startGameButton = document.getElementById('start-game');
    const getHistoryButton = document.getElementById('get-history');
    const cardsContainer = document.getElementById('cards');
    const historyData = document.getElementById('history-data');

    function clearHistory() {
        historyData.textContent = '';
    }

    clearCards();
    clearHistory();

    async function refreshAccessToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            console.error('Токен обновления не найден. Пожалуйста, войдите снова.');
            return;
        }

        try {
            const response = await fetch('/token/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: refreshToken,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access);
                console.log('Токен доступа успешно обновлен.');
            } else {
                console.error('Не удалось обновить токен доступа:', response.statusText);
                localStorage.clear();
                alert('Сессия истекла. Пожалуйста, войдите снова.');
                window.location.href = '/login/';
            }
        } catch (error) {
            console.error('Ошибка при обновлении токена:', error);
        }
    }

    async function fetchWithJWT(url, options = {}) {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            console.error('Токен доступа не найден. Пожалуйста, войдите.');
            return;
        }

        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${accessToken}`,
        };

        const response = await fetch(url, options);

        if (response.status === 401) {
            await refreshAccessToken();
            return fetchWithJWT(url, options);
        }

        return response;
    }

    startGameButton.addEventListener('click', async () => {
        try {
            const response = await fetchWithJWT('/get-cards/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const cards = await response.json();
                displayCards(cards);
            } else {
                console.error('Не удалось получить карты:', response.statusText);
                alert('Не удалось получить карты. Пожалуйста, попробуйте снова.');
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });

    function displayCards(cards) {
        cardsContainer.innerHTML = '';

        cards.forEach(card => {
            const cardElement = document.createElement('div');
            cardElement.className = 'col-md-4 card';
            cardElement.innerHTML = `
                <h3>${card.name}</h3>
                <p>Сила: ${card.strength}</p>
                <p>Ловкость: ${card.agility}</p>
                <p>Интеллект: ${card.intelligence}</p>
                <p>Удача: ${card.luck}</p>
                <button class="btn btn-success choose-card" data-card-id="${card.id}">Выбрать</button>
            `;
            cardsContainer.appendChild(cardElement);
        });

        const chooseButtons = document.querySelectorAll('.choose-card');
        chooseButtons.forEach(button => {
            button.addEventListener('click', async () => {
                const cardId = button.getAttribute('data-card-id');
                await chooseWinner(cardId);
            });
        });
    }

    async function chooseWinner(cardId) {
        const cards = Array.from(cardsContainer.children).map(card => {
            return {
                id: card.querySelector('button').getAttribute('data-card-id'),
                name: card.querySelector('h3').innerText,
            };
        });

        const card1 = cards[0].id;
        const card2 = cards[1].id;

        try {
            const response = await fetchWithJWT('/choose-winner/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    card1: card1,
                    card2: card2,
                    user_choice: cardId,
                }),
            });

            if (response.ok) {
                const result = await response.json();
                alert(`Выйграл: ${result.winner_name}`);
                clearCards();
                clearHistory();
            } else {
                console.error('Ошибка выбора:', response.statusText);
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    }

    getHistoryButton.addEventListener('click', async () => {
        try {
            const response = await fetchWithJWT('/game-history/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const history = await response.json();
                historyData.textContent = JSON.stringify(history, null, 2);
            } else {
                console.error('Ошибка отображения истории:', response.statusText);
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });

    if (!localStorage.getItem('access_token')) {
        window.location.href = '/login/';
    }
});