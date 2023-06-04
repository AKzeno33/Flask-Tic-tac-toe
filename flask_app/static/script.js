var currentPlayer = "X";
var gameActive = true;
var board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
];
var playerScore = parseInt(localStorage.getItem("playerScore")) || 0;
var computerScore = parseInt(localStorage.getItem("computerScore")) || 0;

function makeMove(row, col) {
    if (gameActive && board[row][col] === "") {
        board[row][col] = currentPlayer;
        document.getElementsByClassName("cell")[row * 3 + col].innerHTML = currentPlayer;
        checkGameStatus();
        if (gameActive) {
            togglePlayer();
            makeComputerMove();
        }
    }
}

function togglePlayer() {
    currentPlayer = currentPlayer === "X" ? "O" : "X";
}

function checkGameStatus() {
    var winner = getWinner();
    if (winner) {
        document.getElementById("status").innerHTML = "Player " + winner + " wins!";
        if (winner === "X") {
            playerScore++;
            document.getElementById("playerScore").textContent = playerScore;
        } else {
            computerScore++;
            document.getElementById("computerScore").textContent = computerScore;
        }
        gameActive = false;
    } else if (isBoardFull()) {
        document.getElementById("status").innerHTML = "It's a tie!";
        gameActive = false;
    }
}

function getWinner() {
    var winningCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
        [0, 4, 8], [2, 4, 6] // Diagonals
    ];

    for (var i = 0; i < winningCombinations.length; i++) {
        var [a, b, c] = winningCombinations[i];
        if (board[Math.floor(a / 3)][a % 3] !== "" &&
            board[Math.floor(a / 3)][a % 3] === board[Math.floor(b / 3)][b % 3] &&
            board[Math.floor(a / 3)][a % 3] === board[Math.floor(c / 3)][c % 3]) {
            return board[Math.floor(a / 3)][a % 3];
        }
    }

    return null;
}

function isBoardFull() {
    for (var row = 0; row < 3; row++) {
        for (var col = 0; col < 3; col++) {
            if (board[row][col] === "") {
                return false;
            }
        }
    }
    return true;
}

function makeComputerMove() {
    var availableCells = [];
    for (var row = 0; row < 3; row++) {
        for (var col = 0; col < 3; col++) {
            if (board[row][col] === "") {
                availableCells.push([row, col]);
            }
        }
    }

    if (availableCells.length > 0) {
        var randomIndex = Math.floor(Math.random() * availableCells.length);
        var [row, col] = availableCells[randomIndex];
        board[row][col] = currentPlayer;
        document.getElementsByClassName("cell")[row * 3 + col].innerHTML = currentPlayer;
        checkGameStatus();
        togglePlayer();
    }
}

function resetGame() {
    currentPlayer = "X";
    gameActive = true;
    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ];
    var cells = document.getElementsByClassName("cell");
    for (var i = 0; i < cells.length; i++) {
        cells[i].innerHTML = "";
    }
    document.getElementById("status").innerHTML = "";
    playerScore = 0;
    computerScore = 0;
    document.getElementById("playerScore").textContent = playerScore;
    document.getElementById("computerScore").textContent = computerScore;
    localStorage.setItem("playerScore", playerScore);
    localStorage.setItem("computerScore", computerScore);
}

// Initialize the player and computer scores
document.getElementById("playerScore").textContent = playerScore;
document.getElementById("computerScore").textContent = computerScore;