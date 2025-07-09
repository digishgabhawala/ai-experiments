let playerPosition = 1;
let welcomeScreen;
let gameScreen;
let turnIndicator;
let playButton;
let gameBoard;
let rollDiceButton;

function placePlayer() {
    const currentSquare = document.querySelector(`[data-square="${playerPosition}"]`);
    const playerPiece = document.createElement('div');
    playerPiece.classList.add('player-piece');
    currentSquare.appendChild(playerPiece);
}

document.addEventListener('DOMContentLoaded', () => {
    welcomeScreen = document.getElementById('welcome-screen');
    gameScreen = document.getElementById('game-screen');
    turnIndicator = document.getElementById('turn-indicator');
    playButton = document.getElementById('play-button');
    gameBoard = document.getElementById('game-board');
    rollDiceButton = document.getElementById('roll-dice-button');

    function createBoard() {
        for (let i = 1; i <= 100; i++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.dataset.square = i;
            square.textContent = i;
            gameBoard.appendChild(square);
        }
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

        let newPosition = playerPosition + diceRoll;

        if (newPosition > 100) {
            newPosition = playerPosition; // Player remains at current position if roll overshoots 100
        }

        // Remove player piece from current square
        const currentPlayerPiece = document.querySelector('.player-piece');
        if (currentPlayerPiece) {
            currentPlayerPiece.remove();
        }

        playerPosition = newPosition;
        placePlayer();
    });

    createBoard();
});