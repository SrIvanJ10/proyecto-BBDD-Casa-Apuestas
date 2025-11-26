// Datos de ejemplo 
const appData = {
    matches: [
        {
            id: 1,
            sport: "Fútbol",
            team1: "Real Madrid",
            team2: "FC Barcelona",
            date: "2025-10-20T20:00:00",
            odds: {
                team1: 2.10,
                draw: 3.25,
                team2: 3.40
            }
        },
        {
            id: 2,
            sport: "Baloncesto",
            team1: "Los Angeles Lakers",
            team2: "Golden State Warriors",
            date: "2025-10-21T22:30:00",
            odds: {
                team1: 1.85,
                team2: 1.95
            }
        },
        {
            id: 3,
            sport: "Fútbol",
            team1: "Manchester City",
            team2: "Liverpool FC",
            date: "2025-10-22T15:00:00",
            odds: {
                team1: 2.30,
                draw: 3.10,
                team2: 3.00
            }
        }
    ],

    userBets: [
        {
            id: 1,
            match: "Real Madrid vs FC Barcelona",
            selection: "Real Madrid",
            odd: 2.10,
            amount: 50,
            status: "pending"
        },
        {
            id: 2,
            match: "Lakers vs Warriors",
            selection: "Warriors",
            odd: 1.95,
            amount: 30,
            status: "won"
        }
    ],

    ranking: [
        { position: 1, username: "betMaster", correctBets: 42, percentage: "78%", points: 1250 },
        { position: 2, username: "goalHunter", correctBets: 38, percentage: "72%", points: 1100 },
        { position: 3, username: "ballExpert", correctBets: 35, percentage: "68%", points: 980 },
        { position: 4, username: "sportFan", correctBets: 32, percentage: "65%", points: 850 },
        { position: 5, username: "luckyBettor", correctBets: 29, percentage: "62%", points: 720 }
    ],

    recommendations: [
        {
            match: "Real Madrid vs FC Barcelona",
            recommendation: "Victoria Local",
            confidence: "Alta",
            reason: "Mejor forma actual del equipo local"
        },
        {
            match: "Lakers vs Warriors",
            recommendation: "Total Puntos Over",
            confidence: "Media",
            reason: "Ambos equipos con ofensivas fuertes"
        }
    ]
};

// Estado de la aplicación
let selectedOdds = {};

// Funciones de renderizado
function renderMatches() {
    const container = document.getElementById('matches');
    container.innerHTML = '';

    appData.matches.forEach(match => {
        const matchCard = document.createElement('div');
        matchCard.className = 'match-card';

        const isFootball = match.sport === "Fútbol";

        matchCard.innerHTML = `
            <div class="match-header">
                <span class="sport-badge">${match.sport}</span>
                <span class="match-date">${formatDate(match.date)}</span>
            </div>
            <div class="teams">
                <h3>${match.team1} vs ${match.team2}</h3>
            </div>
            <div class="odds">
                <button class="odd-btn" data-match="${match.id}" data-selection="team1">
                    ${match.team1}<br><strong>${match.odds.team1}</strong>
                </button>
                ${isFootball ? `
                <button class="odd-btn" data-match="${match.id}" data-selection="draw">
                    Empate<br><strong>${match.odds.draw}</strong>
                </button>
                ` : ''}
                <button class="odd-btn" data-match="${match.id}" data-selection="team2">
                    ${match.team2}<br><strong>${match.odds.team2}</strong>
                </button>
            </div>
            <button class="btn btn-primary place-bet" data-match="${match.id}">
                Realizar Apuesta
            </button>
        `;

        container.appendChild(matchCard);
    });

    // Event listeners para selección de cuotas
    document.querySelectorAll('.odd-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const matchId = this.getAttribute('data-match');
            const selection = this.getAttribute('data-selection');

            // Deseleccionar otros botones del mismo partido
            document.querySelectorAll(`.odd-btn[data-match="${matchId}"]`).forEach(b => {
                b.classList.remove('selected');
            });

            // Seleccionar este botón
            this.classList.add('selected');
            selectedOdds[matchId] = selection;
        });
    });

    // Event listeners para botones de apuesta
    document.querySelectorAll('.place-bet').forEach(btn => {
        btn.addEventListener('click', function () {
            const matchId = this.getAttribute('data-match');
            const selection = selectedOdds[matchId];

            if (selection) {
                const match = appData.matches.find(m => m.id == matchId);
                const amount = prompt(`¿Cuánto quieres apostar por ${getSelectionName(selection, match)}?`);

                if (amount && !isNaN(amount) && amount > 0) {
                    alert(`¡Apuesta realizada!\n${match.team1} vs ${match.team2}\nApuesta: ${getSelectionName(selection, match)}\nCantidad: ${amount}€`);
                }
            } else {
                alert('Por favor, selecciona una opción antes de apostar');
            }
        });
    });
}

function renderBets() {
    const container = document.getElementById('bets');

    if (appData.userBets.length === 0) {
        container.innerHTML = '<p class="no-bets">No tienes apuestas realizadas</p>';
        return;
    }

    container.innerHTML = '';
    appData.userBets.forEach(bet => {
        const betCard = document.createElement('div');
        betCard.className = 'bet-card';

        betCard.innerHTML = `
            <div class="bet-info">
                <h3>${bet.match}</h3>
                <p>Apuesta: ${bet.selection} (Cuota: ${bet.odd})</p>
                <p>Cantidad: ${bet.amount}€</p>
            </div>
            <div class="bet-status">${bet.status === 'won' ? 'Ganada' : 'Pendiente'}</div>
        `;

        container.appendChild(betCard);
    });
}

function renderRanking() {
    const tbody = document.getElementById('rankingBody');
    tbody.innerHTML = '';

    appData.ranking.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.position}</td>
            <td>${user.username}</td>
            <td>${user.correctBets}</td>
            <td>${user.percentage}</td>
            <td>${user.points}</td>
        `;
        tbody.appendChild(row);
    });
}

function renderRecommendations() {
    const container = document.getElementById('recommendations');
    container.innerHTML = '';

    appData.recommendations.forEach(rec => {
        const recCard = document.createElement('div');
        recCard.className = 'recommendation-card';

        recCard.innerHTML = `
            <span class="confidence-badge">Confianza: ${rec.confidence}</span>
            <h3>${rec.match}</h3>
            <p><strong>Recomendación:</strong> ${rec.recommendation}</p>
            <p><strong>Razón:</strong> ${rec.reason}</p>
        `;

        container.appendChild(recCard);
    });
}

// Funciones auxiliares
function formatDate(dateString) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

function getSelectionName(selection, match) {
    switch (selection) {
        case 'team1': return match.team1;
        case 'team2': return match.team2;
        case 'draw': return 'Empate';
        default: return selection;
    }
}

// Event listeners globales
document.getElementById('login').addEventListener('click', function () {
    alert('Funcionalidad de login en desarrollo');
});

document.getElementById('register').addEventListener('click', function () {
    alert('Funcionalidad de registro en desarrollo');
});

document.getElementById('comenzar').addEventListener('click', function () {
    document.getElementById('partidos').scrollIntoView({
        behavior: 'smooth'
    });
});

document.getElementById('contact').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Formulario enviado correctamente');
    this.reset();
});

// Navegación 
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Inicialización
document.addEventListener('DOMContentLoaded', function () {
    renderMatches();
    renderBets();
    renderRanking();
    renderRecommendations();

    console.log('Sport 365 - Frontend inicializado');
});