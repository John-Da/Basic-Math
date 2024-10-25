document.addEventListener('DOMContentLoaded', () => {
    const modeBtns = document.querySelectorAll('.start-btn');
    
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const selectedMode = btn.dataset.mode;
            localStorage.setItem('selectedMode', selectedMode);
            window.location.href = 'operation.html';
        });
    });
});