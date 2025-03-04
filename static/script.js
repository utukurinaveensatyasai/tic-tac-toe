document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll(".cell");
    const status = document.getElementById("status");
    const resetButton = document.getElementById("reset");
    let currentPlayer = "X";
    let board = ["", "", "", "", "", "", "", "", ""];
    let gameActive = true;

    function checkWinner() {
        const winningCombos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ];

        for (let combo of winningCombos) {
            let [a, b, c] = combo;
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                status.textContent = `${currentPlayer} Wins! 🎉`;
                gameActive = false;
                return;
            }
        }
        
        if (!board.includes("")) {
            status.textContent = "It's a Draw! 🤝";
            gameActive = false;
        }
    }

    function handleClick(event) {
        if (!gameActive) return;
        const index = event.target.dataset.index;
        
        if (board[index] === "") {
            board[index] = currentPlayer;
            event.target.textContent = currentPlayer;
            checkWinner();
            currentPlayer = currentPlayer === "X" ? "O" : "X";
            if (gameActive) status.textContent = `Player ${currentPlayer}'s Turn`;
        }
    }

    function resetGame() {
        board = ["", "", "", "", "", "", "", "", ""];
        gameActive = true;
        currentPlayer = "X";
        status.textContent = "Your Turn (X)";
        cells.forEach(cell => cell.textContent = "");
    }

    cells.forEach(cell => cell.addEventListener("click", handleClick));
    resetButton.addEventListener("click", resetGame);
});
