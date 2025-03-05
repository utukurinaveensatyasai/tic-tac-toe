document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll(".cell");
    const status = document.getElementById("status");
    const resetButton = document.getElementById("reset");

    let gameActive = true;

    function updateBoard(board) {
        board.forEach((value, index) => {
            cells[index].textContent = value !== " " ? value : "";
        });
    }

    function checkGameStatus(response) {
        if (response.status === "win") {
            status.textContent = `${response.winner} Wins! 🎉`;
            gameActive = false;
        } else if (response.status === "draw") {
            status.textContent = "It's a Draw! 🤝";
            gameActive = false;
        } else {
            status.textContent = `Player X's Turn`;
        }
    }

    async function handleClick(event) {
        if (!gameActive) return;

        const index = event.target.dataset.index;
        const row = Math.floor(index / 3);
        const col = index % 3;

        // Make sure the clicked cell is empty
        if (event.target.textContent !== "") return;

        try {
            // Send move to backend
            const response = await fetch("/move", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ row, col })
            });

            const data = await response.json();
            updateBoard(data.board);
            checkGameStatus(data);
        } catch (error) {
            console.error("Error:", error);
        }
    }

    async function resetGame() {
        try {
            const response = await fetch("/reset", {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            });

            const data = await response.json();
            updateBoard(data.board);
            status.textContent = "Your Turn (X)";
            gameActive = true;
        } catch (error) {
            console.error("Error:", error);
        }
    }

    // Attach event listeners
    cells.forEach(cell => cell.addEventListener("click", handleClick));
    resetButton.addEventListener("click", resetGame);
});
