// Game configuration
const GAME_CONFIG = {
    basePoints: {
        easy: 10,
        medium: 20,
        hard: 30
    },
    streakBonus: {
        threshold: 3,
        multiplier: 1.5,
        maxStreak: 10
    },
    difficulties: {
        easy: { 
            timeLimit: 60, 
            range: { min: 1, max: 12 },
            timePenalty: 3,
            bonusTime: 2
        },
        medium: { 
            timeLimit: 45, 
            range: { min: 1, max: 25 },
            timePenalty: 4,
            bonusTime: 1
        },
        hard: { 
            timeLimit: 30, 
            range: { min: 1, max: 50 },
            timePenalty: 5,
            bonusTime: 1
        }
    },
    animations: {
        duration: 400,
        scoreIncrement: 25
    }
};

// Game state
const gameState = {
    score: 0,
    timeLeft: GAME_CONFIG.difficulties.easy.timeLimit,
    currentProblem: null,
    isGameActive: false,
    timer: null,
    highScore: parseInt(localStorage.getItem('highScore')) || 0,
    selectedMode: localStorage.getItem('selectedMode') || 'addition',
    selectedDifficulty: localStorage.getItem('selectedDifficulty') || 'easy',
    streak: 0,
    bestStreak: 0,
    totalQuestions: 0,
    correctAnswers: 0,
    isPaused: false,
    soundEnabled: localStorage.getItem('soundEnabled') === 'true'
};


// Audio Manager
const gameAudio = {
    sounds: {
        correct: new Audio('./assets/audios/correct.mp3'),
        wrong: new Audio('./assets/audios/wrong.mp3'),
        gameOver: new Audio('./assets/audios/gameover.mp3'),
        theme: new Audio('./assets/audios/Test1.mp3')
    },

    init() {
        // Configure theme music
        this.sounds.theme.loop = true;
        this.sounds.theme.volume = 0.3;

        // Configure sound effects
        this.sounds.correct.volume = 0.5;
        this.sounds.wrong.volume = 0.5;
        this.sounds.gameOver.volume = 0.5;

        // Preload all sounds
        Object.values(this.sounds).forEach(sound => {
            sound.load();
        });
    },

    play(soundName) {
        if (gameState.soundEnabled && this.sounds[soundName]) {
            // Stop and reset the sound before playing
            this.sounds[soundName].currentTime = 0;
            this.sounds[soundName].play().catch(err => console.log('Audio play failed:', err));
        }
    },

    playTheme() {
        if (gameState.soundEnabled) {
            this.sounds.theme.play().catch(err => console.log('Theme play failed:', err));
        }
    },

    pauseTheme() {
        this.sounds.theme.pause();
        this.sounds.theme.currentTime = 0;
    }
};


let elements = null;

// DOM Elements for gameplay
function getElements() {
    return {
        gameScreen: document.getElementById('gameScreen'),
        problem: document.getElementById('problem'),
        score: document.getElementById('score'),
        time: document.getElementById('time'),
        highScore: document.getElementById('highScore'),
        message: document.getElementById('message'),
        progressBar: document.getElementById('progressBar'),
        pauseBtn: document.querySelector('.game-controls button:first-child'),
        soundBtn: document.querySelector('.game-controls button:last-child'),
        answerbtn: document.getElementById('answerbtn')
    };
}

async function initializeGame() {
    try {
        elements = getElements();
        
        // Initialize audio
        await gameAudio.init();
        
        // Add event listeners
        elements.pauseBtn.addEventListener('click', togglePause);
        elements.soundBtn.addEventListener('click', toggleSound);
        
        // Set initial button states
        elements.pauseBtn.textContent = '⏸️';
        elements.soundBtn.textContent = gameState.soundEnabled ? '🔊' : '🔇';
        
        // Start theme music if enabled
        if (gameState.soundEnabled) {
            gameAudio.playTheme();
        }
        
        startGame();
    } catch (error) {
        console.error('Failed to initialize game:', error);
        showError('Failed to initialize game. Please refresh the page.');
    }
}

function startGame() {
    Object.assign(gameState, {
        score: 0,
        streak: 0,
        bestStreak: 0,
        totalQuestions: 0,
        correctAnswers: 0,
        timeLeft: GAME_CONFIG.difficulties[gameState.selectedDifficulty].timeLimit,
        isGameActive: true,
        isPaused: false
    });
    
    updateUI();
    updateProgressBar();
    newQuestion();
    startTimer();
}

function generateProblem() {
    const difficulty = GAME_CONFIG.difficulties[gameState.selectedDifficulty];
    const range = difficulty.range;
    let num1 = Math.floor(Math.random() * (range.max - range.min + 1)) + range.min;
    let num2 = Math.floor(Math.random() * (range.max - range.min + 1)) + range.min;
    
    const problem = {
        num1,
        num2,
        operation: '',
        expression: '',
        answer: 0
    };
    
    let mode = gameState.selectedMode;
    if (mode === 'random') {
        const operations = ['addition', 'subtraction', 'multiplication', 'division'];
        mode = operations[Math.floor(Math.random() * operations.length)];
    }
    
    switch (mode) {
        case 'addition':
            problem.operation = '+';
            problem.answer = num1 + num2;
            problem.expression = `${num1} + ${num2}`;
            break;
            
        case 'subtraction':
            if (num1 < num2) [num1, num2] = [num2, num1];
            problem.num1 = num1;
            problem.num2 = num2;
            problem.operation = '-';
            problem.answer = num1 - num2;
            problem.expression = `${num1} - ${num2}`;
            break;
            
        case 'multiplication':
            problem.operation = '×';
            problem.answer = num1 * num2;
            problem.expression = `${num1} × ${num2}`;
            break;
            
        case 'division':
            const product = num1 * num2;
            problem.num1 = product;
            problem.num2 = num2;
            problem.operation = '÷';
            problem.answer = num1;
            problem.expression = `${product} ÷ ${num2}`;
            break;
    }
    
    return problem;
}

// Generate wrong answers that are close to the correct answer

function generateWrongAnswers(correctAnswer, operationType) {
    const wrongAnswers = new Set();
    const range = Math.max(Math.floor(correctAnswer * 0.5), 5);

    while (wrongAnswers.size < 3) {
        let wrongAnswer;
        const randomOffset = Math.floor(Math.random() * range) - Math.floor(range / 2);
        
        if (operationType === 'multiplication' || operationType === 'division') {
            wrongAnswer = correctAnswer + (randomOffset > 0 ? randomOffset + 1 : randomOffset - 1);
        } else {
            wrongAnswer = correctAnswer + randomOffset;
        }

        if (wrongAnswer > 0 && wrongAnswer !== correctAnswer) {
            wrongAnswers.add(wrongAnswer);
        }
    }

    return Array.from(wrongAnswers);
}

function showError(message) {
    showMessage(message, 'error');
}

// Update the newQuestion function to handle multiple choice
function newQuestion() {
    gameState.currentProblem = generateProblem();
    elements.problem.textContent = gameState.currentProblem.expression;
    
    const wrongAnswers = generateWrongAnswers(
        gameState.currentProblem.answer, 
        gameState.selectedMode
    );
    
    const allAnswers = [gameState.currentProblem.answer, ...wrongAnswers];
    const shuffledAnswers = shuffleArray(allAnswers);
    
    elements.answerbtn.innerHTML = shuffledAnswers.map(answer => 
        `<button class="ansbtn" onclick="checkAnswer(${answer})">${answer}</button>`
    ).join('');
}

// Shuffle array function
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Modified checkAnswer function for button clicks
function checkAnswer(userAnswer) {
    if (!gameState.isGameActive || gameState.isPaused) return;
    
    gameState.totalQuestions++;
    const difficulty = GAME_CONFIG.difficulties[gameState.selectedDifficulty];
    
    if (userAnswer === gameState.currentProblem.answer) {
        handleCorrectAnswer(difficulty);
    } else {
        handleWrongAnswer(difficulty);
    }
    
    updateUI();
    newQuestion();
}

// Toggle pause state
function togglePause() {
    if (!gameState.isGameActive) return;

    gameState.isPaused = !gameState.isPaused;
    elements.pauseBtn.textContent = gameState.isPaused ? '▶️' : '⏸️';

    if (gameState.isPaused) {
        clearInterval(gameState.timer);
        pauseDialog();
    } else {
        removePauseDialog(); 
        startTimer();
    }
}

function pauseDialog() {
    const pDia = document.createElement('div');
    pDia.className = 'pause-dialog';
    pDia.innerHTML = `
    <h2>Do you want to leave?</h2>
    <div class="button-group">
        <button onclick="togglePause()" class="playagain-btn">Resume</button>
        <button onclick="window.location.href='operation.html'" class="mainmenu-btn">Main Menu</button>
    </div>
    `;
    document.body.appendChild(pDia);

    requestAnimationFrame(() => pDia.classList.add('visible'));
}

function removePauseDialog() {
    const dialog = document.querySelector('.pause-dialog');
    if (dialog) {
        document.body.removeChild(dialog);
    }
}

function toggleSound() {
    gameState.soundEnabled = !gameState.soundEnabled;
    localStorage.setItem('soundEnabled', gameState.soundEnabled);
    elements.soundBtn.textContent = gameState.soundEnabled ? '🔊' : '🔇';
    
    if (gameState.soundEnabled) {
        gameAudio.playTheme();
    } else {
        gameAudio.pauseTheme();
    }
}

function initializeGame() {
    try {
        elements = getElements();
        
        // Add event listeners
        elements.pauseBtn.addEventListener('click', togglePause);
        elements.soundBtn.addEventListener('click', toggleSound);
        
        // Set initial button states
        elements.pauseBtn.textContent = '⏸️';
        elements.soundBtn.textContent = gameState.soundEnabled ? '🔊' : '🔇';
        
        startGame();
    } catch (error) {
        console.error('Failed to initialize game:', error);
        showError('Failed to initialize game. Please refresh the page.');
    }
}


function startTimer() {
    if (gameState.timer) {
        clearInterval(gameState.timer);
    }
    
    gameState.timer = setInterval(() => {
        if (gameState.isPaused) return;
        
        gameState.timeLeft--;
        updateProgressBar();
        elements.time.textContent = gameState.timeLeft;
        
        if (gameState.timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function updateProgressBar() {
    const difficultyConfig = GAME_CONFIG.difficulties[gameState.selectedDifficulty];
    const percentage = (gameState.timeLeft / difficultyConfig.timeLimit) * 100;
    elements.progressBar.style.width = `${percentage}%`;
}

function checkAnswer(userAnswer) {
    if (!gameState.isGameActive || gameState.isPaused) return;
    
    gameState.totalQuestions++;
    const difficulty = GAME_CONFIG.difficulties[gameState.selectedDifficulty];
    
    if (userAnswer === gameState.currentProblem.answer) {
        handleCorrectAnswer(difficulty);
    } else {
        handleWrongAnswer(difficulty);
    }
    
    updateUI();
    newQuestion();
}

function handleCorrectAnswer(difficulty) {
    gameState.correctAnswers++;
    gameState.streak = Math.min(gameState.streak + 1, GAME_CONFIG.streakBonus.maxStreak);
    gameState.bestStreak = Math.max(gameState.streak, gameState.bestStreak);
    
    if (gameState.soundEnabled) {
        gameAudio.play('correct');
    }
    
    const basePoints = GAME_CONFIG.basePoints[gameState.selectedDifficulty];
    const streakMultiplier = gameState.streak >= GAME_CONFIG.streakBonus.threshold ? 
        Math.min(GAME_CONFIG.streakBonus.multiplier * 
            (1 + (gameState.streak - GAME_CONFIG.streakBonus.threshold) * 0.1), 2) : 1;
    
    const pointsEarned = Math.round(basePoints * streakMultiplier);
    gameState.score += pointsEarned;
    
    gameState.timeLeft = Math.min(
        gameState.timeLeft + difficulty.bonusTime,
        GAME_CONFIG.difficulties[gameState.selectedDifficulty].timeLimit
    );
    
    const streakMsg = streakMultiplier > 1 ? 
        ` (${gameState.streak}x Streak!)` : '';
    showMessage(`Correct! +${pointsEarned}${streakMsg}`, 'success');
}

function handleWrongAnswer(difficulty) {
    gameState.streak = 0;
    gameState.timeLeft = Math.max(0, gameState.timeLeft - difficulty.timePenalty);
    
    if (gameState.soundEnabled) {
        gameAudio.play('wrong');
    }
    
    const wrongButton = document.querySelector(`.ansbtn[onclick="checkAnswer(${gameState.currentProblem.answer})"]`);
    if (wrongButton) {
        wrongButton.classList.add('shake');
        setTimeout(() => wrongButton.classList.remove('shake'), 500);
    }
    
    showMessage(`Wrong! The answer was ${gameState.currentProblem.answer}`, 'error');
}
function endGame() {
    if (!gameState.isGameActive) return;
    
    if (gameState.soundEnabled) {
        gameAudio.play('gameOver');
    }
    
    gameState.isGameActive = false;
    clearInterval(gameState.timer);
    gameState.timer = null;
    
    elements.answerbtn.style.pointerEvents = 'none';
    
    if (gameState.score > gameState.highScore) {
        gameState.highScore = gameState.score;
        localStorage.setItem('highScore', gameState.highScore);
        showGameOverDialog(`🎉 New High Score: ${gameState.score}!`);
    } else {
        showGameOverDialog(`Game Over! Score: ${gameState.score}`);
    }
    
    gameAudio.pauseTheme();
}

function showGameOverDialog(message) {
    const accuracy = ((gameState.correctAnswers / gameState.totalQuestions) * 100).toFixed(1);
    const avgTimePerQuestion = ((GAME_CONFIG.difficulties[gameState.selectedDifficulty].timeLimit - 
        gameState.timeLeft) / gameState.totalQuestions).toFixed(1);
    
    const dialog = document.createElement('div');
    dialog.className = 'game-over-dialog';
    dialog.innerHTML = `
        <h2>${message}</h2>
        <div class="stats-grid">
            <div class="stat-item">
                <span class="label">Questions</span>
                <span class="value">${gameState.totalQuestions}</span>
            </div>
            <div class="stat-item">
                <span class="label">Correct</span>
                <span class="value">${gameState.correctAnswers}</span>
            </div>
            <div class="stat-item">
                <span class="label">Accuracy</span>
                <span class="value">${accuracy}%</span>
            </div>
            <div class="stat-item">
                <span class="label">Best Streak</span>
                <span class="value">${gameState.bestStreak}</span>
            </div>
            <div class="stat-item">
                <span class="label">Avg Time/Q</span>
                <span class="value">${avgTimePerQuestion}s</span>
            </div>
            <div class="stat-item">
                <span class="label">Final Score</span>
                <span class="value">${gameState.score}</span>
            </div>
        </div>
        <div class="button-group">
            <button onclick="location.reload()" class="playagain-btn">Play Again</button>
            <button onclick="window.location.href='operation.html'" class="mainmenu-btn">Main Menu</button>
        </div>
    `;
    
    document.body.appendChild(dialog);
    requestAnimationFrame(() => dialog.classList.add('visible'));
}

function showMessage(text, type) {
    elements.message.textContent = text;
    elements.message.className = `message ${type}`;
    setTimeout(() => {
        elements.message.textContent = '';
        elements.message.className = 'message';
    }, 2000);
}

function updateUI() {
    elements.score.textContent = gameState.score;
    elements.time.textContent = gameState.timeLeft;
    elements.highScore.textContent = gameState.highScore;
}

document.addEventListener('DOMContentLoaded', initializeGame);