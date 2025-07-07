document.addEventListener('DOMContentLoaded', () => {
    const welcomeScreen = document.getElementById('welcome-screen');
    const gameScreen = document.getElementById('game-screen');
    const playButton = document.getElementById('play-button');

    playButton.addEventListener('click', () => {
        welcomeScreen.classList.add('hidden');
        gameScreen.classList.remove('hidden');
    });
});