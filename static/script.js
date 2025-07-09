let playerPosition = 1;
let welcomeScreen;
let gameScreen;
let turnIndicator;
let playButton;
let gameBoard;
let rollDiceButton;
let gameLinesSvg;
let winningCelebration;
let playAgainButton;

const SNAKES_AND_LADDERS = [
    { start: 16, end: 6, type: 'snake' },
    { start: 47, end: 26, type: 'snake' },
    { start: 49, end: 11, type: 'snake' },
    { start: 56, end: 53, type: 'snake' },
    { start: 62, end: 19, type: 'snake' },
    { start: 64, end: 60, type: 'snake' },
    { start: 87, end: 24, type: 'snake' },
    { start: 93, end: 73, type: 'snake' },
    { start: 95, end: 75, type: 'snake' },
    { start: 98, end: 78, type: 'snake' },
    { start: 1, end: 38, type: 'ladder' },
    { start: 4, end: 14, type: 'ladder' },
    { start: 9, end: 31, type: 'ladder' },
    { start: 21, end: 42, type: 'ladder' },
    { start: 28, end: 84, type: 'ladder' },
    { start: 36, end: 44, type: 'ladder' },
    { start: 51, end: 67, type: 'ladder' },
    { start: 71, end: 91, type: 'ladder' },
    { start: 80, end: 100, type: 'ladder' }
];

function placePlayer() {
    const currentSquare = document.querySelector(`[data-square="${playerPosition}"]`);
    let playerPiece = document.querySelector('.player-piece'); // Try to find existing piece

    if (!playerPiece) { // If no piece exists, create one
        playerPiece = document.createElement('div');
        playerPiece.classList.add('player-piece');
    } else { // If piece exists, remove from old parent
        playerPiece.remove();
    }
    currentSquare.appendChild(playerPiece);
}

function drawSnakeLadderLines() {
    SNAKES_AND_LADDERS.forEach(sl => {
        const startSquare = document.querySelector(`[data-square="${sl.start}"]`);
        const endSquare = document.querySelector(`[data-square="${sl.end}"]`);

        if (startSquare && endSquare) {
            const startRect = startSquare.getBoundingClientRect();
            const endRect = endSquare.getBoundingClientRect();
            const gameBoardRect = gameBoard.getBoundingClientRect();

            const x1 = startRect.left + startRect.width / 2 - gameBoardRect.left;
            const y1 = startRect.top + startRect.height / 2 - gameBoardRect.top;
            const x2 = endRect.left + endRect.width / 2 - gameBoardRect.left;
            const y2 = endRect.top + endRect.height / 2 - gameBoardRect.top;

            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', x1);
            line.setAttribute('y1', y1);
            line.setAttribute('x2', x2);
            line.setAttribute('y2', y2);
            line.setAttribute('stroke', sl.type === 'snake' ? 'red' : 'green');
            line.setAttribute('stroke-width', '4');
            gameLinesSvg.appendChild(line);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    welcomeScreen = document.getElementById('welcome-screen');
    gameScreen = document.getElementById('game-screen');
    turnIndicator = document.getElementById('turn-indicator');
    playButton = document.getElementById('play-button');
    gameBoard = document.getElementById('game-board');
    rollDiceButton = document.getElementById('roll-dice-button');
    gameLinesSvg = document.getElementById('game-lines');
    winningCelebration = document.getElementById('winning-celebration');
    playAgainButton = document.getElementById('play-again-button');

    function createBoard() {
        for (let i = 1; i <= 100; i++) {
            const square = document.createElement('div');
            square.classList.add('square');
            square.dataset.square = i;
            square.textContent = i;
            gameBoard.appendChild(square);
        }
    }

    function resetGame() {
        playerPosition = 1;
        placePlayer(); // Place player on square 1
        winningCelebration.classList.add('hidden');
        welcomeScreen.classList.remove('hidden');
    }

    playButton.addEventListener('click', () => {
        welcomeScreen.classList.add('hidden');
        gameScreen.classList.remove('hidden');
        turnIndicator.textContent = "Your Turn";
        placePlayer();
        drawSnakeLadderLines();
    });

    playAgainButton.addEventListener('click', () => {
        resetGame();
    });

    rollDiceButton.addEventListener('click', () => {
        const diceRoll = Math.floor(Math.random() * 6) + 1;
        turnIndicator.textContent = `You rolled a ${diceRoll}!`;

        let newPosition = playerPosition + diceRoll;

        if (newPosition > 100) {
            newPosition = playerPosition; // Player remains at current position if roll overshoots 100
        }

        playerPosition = newPosition;
        
        // Check for snakes and ladders
        const snakeLadder = SNAKES_AND_LADDERS.find(sl => sl.start === playerPosition);
        if (snakeLadder) {
            playerPosition = snakeLadder.end;
        }

        placePlayer();

        // Check for win condition
        if (playerPosition === 100) {
            gameScreen.classList.add('hidden');
            winningCelebration.classList.remove('hidden');
        }
    });

    createBoard();
});