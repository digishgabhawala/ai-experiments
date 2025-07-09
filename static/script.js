document.addEventListener('DOMContentLoaded', () => {
    const welcomeScreen = document.getElementById('welcome-screen');
    const gameScreen = document.getElementById('game-screen');
    const turnIndicator = document.getElementById('turn-indicator');
    const playButton = document.getElementById('play-button');
    const gameBoard = document.getElementById('game-board');
    const rollDiceButton = document.getElementById('roll-dice-button');

    let playerPosition = 1;

    function createBoard() {
        for (let i = 1; i <= 100; i++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.dataset.square = i;
            square.textContent = i;
            gameBoard.appendChild(square);
        }
    }

    function placePlayer() {
        const currentSquare = document.querySelector(`[data-square="${playerPosition}"]`);
        const playerPiece = document.createElement('div');
        playerPiece.classList.add('player-piece');
        currentSquare.appendChild(playerPiece);
    }

    playButton.addEventListener('click', () => {
        welcomeScreen.classList.add('hidden');
        gameScreen.classList.remove('hidden');
        turnIndicator.textContent = "Your Turn";
        placePlayer();
    });

    rollDiceButton.addEventListener('click', () => {
        const diceRoll = Math.floor(Math.random() * 6) + 1;
        turnIndicator.textContent = `You rolled a ${diceRoll}!`;
    });

    createBoard();
});