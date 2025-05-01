let currentPlayer = 'X';

function makeMove(row, col) {
    const cell = document.getElementById(`cell-${row}-${col}`);
    if (cell.classList.contains('taken')) return;

    cell.textContent = currentPlayer;
    cell.classList.add('taken');

    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row, col, player: currentPlayer })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('message').textContent = 'Invalid move!';
        } else if (data.winner) {
            document.getElementById('message').textContent = `${data.winner} wins!`;
            document.querySelectorAll('td').forEach(cell => cell.classList.add('taken'));
        } else if (data.draw) {
            document.getElementById('message').textContent = 'It\'s a draw!';
        } else {
            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        }
    })
    .catch(err => {
        console.error('Error:', err);
        document.getElementById('message').textContent = 'Something went wrong!';
    });
}
