document.addEventListener('DOMContentLoaded', () => {
    const difficultyBtns = document.querySelectorAll('.difficulty-btn');
    const backToOperationBtn = document.getElementById('backToOperation');

    difficultyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const selectedDifficulty = btn.dataset.difficulty;
            // Store the selected difficulty in localStorage
            localStorage.setItem('selectedDifficulty', selectedDifficulty);
            // Redirect to game page
            window.location.href = 'gameplay.html';
        });
    });

    backToOperationBtn.addEventListener('click', () => {
        window.location.href = 'operation.html';
    });
});