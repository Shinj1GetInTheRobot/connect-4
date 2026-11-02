const board = document.getElementById("board");
const gameFile = document.getElementById("gameFile");
const resetButton = document.getElementById("reset");
const backButton = document.getElementById("back");
const nextButton = document.getElementById("next");
const endButton = document.getElementById("end");
const moveFilterInput = document.getElementById('moveFilter');


// Game state
let games = null;
let filteredGames = null;
let game = null;
let currentMove = 0;
let currentGame = 0;''

const activeResults = new Set([1, 0, -1]);
const activeMoveTypes = new Set(['h', 'v', 'd1', 'd2']);

loadPage();

function loadPage() {
  for (let row = 0; row < 6; row++) {
    for (let col = 0; col < 7; col++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.dataset.row = row;
      cell.dataset.col = col;
      board.appendChild(cell);
    }
  }
}

function getFilteredGames() {
  const moveFilterText = moveFilterInput.value.trim();
  const wantedMoves = (moveFilterText === '') ? null : Number(moveFilterText);
  return games.filter(game => {
    return activeResults.has(game["result"]) &&
    (wantedMoves === null || wantedMoves < 7 || game["num_moves"] == wantedMoves) &&
    (game["result"] === 0 || [...activeMoveTypes].some(c => game["winning_move_type"] === undefined || game["winning_move_type"].includes(c)))
  });                                       // ^^ check is null for backwards compatibility :)
    
}

// Load a JSON game file
gameFile.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    const text = await file.text();
    const data = JSON.parse(text);
    validateGames(data);
    currentMove = 0;
    currentGame = 0;
    games = Object.values(data);
    filteredGames = getFilteredGames();
    game = games[currentGame];
    renderBoard();
    renderStats();
  } catch (error) {
    alert("Could not load game: " + error.message);
  }
});

// Setup the move filter input bar
moveFilterInput.addEventListener('input', applyFilter);
// Setup win/draws/losses buttons
document.querySelectorAll('.filter-btn-WDL').forEach(btn => {
  btn.addEventListener('click', () => {
    const r = Number(btn.dataset.result);
    const turnOn = !activeResults.has(r);
    if (turnOn) activeResults.add(r);
    else activeResults.delete(r);
    const linked = document.querySelectorAll(`.filter-btn-WDL[data-result="${btn.dataset.result}"]`);
    linked.forEach(b => b.classList.toggle('active', turnOn));
    applyFilter();
  });
});
// Setup move type filter buttons
document.querySelectorAll('.filter-btn-MT').forEach(btn => {
  btn.addEventListener('click', () => {
    const r = btn.dataset.result;
    const turnOn = !activeMoveTypes.has(r);
    if (turnOn) activeMoveTypes.add(r);
    else activeMoveTypes.delete(r);
    btn.classList.toggle('active', turnOn);
    applyFilter();
  });
});

// Filter games from win/draw/loss buttons
function applyFilter() {
  if (games == null) return;
  const text = moveFilterInput.value.trim();
  const wantedMoves = text === '' ? null : Number(text);
  filteredGames = getFilteredGames();
  currentGame = 0;
  currentMove = 0;
  game = filteredGames[currentGame];
  renderBoard();
  renderStats();
}


// Check that the JSON has the expected structure
function validateGames(data) {
  if (!data || typeof data !== "object") {
    throw new Error("The JSON must contain a game object.");
  }
  for (const game of Object.values(data)) {
    if (!Number.isInteger(game.rows) || game.rows <= 0) {
      throw new Error("rows must be a positive integer.");
    }
    if (!Number.isInteger(game.columns) || game.columns <= 0) {
      throw new Error("columns must be a positive integer.");
    }
    if (!Array.isArray(game.moves)) {
      throw new Error("moves must be an array.");
    }
    if (game.moves.length > game.rows * game.columns) {
      throw new Error("There are more moves than board cells.");
    }
    for (const move of game.moves) {
      if (
        !Number.isInteger(move) ||
        move < 0 ||
        move >= game.columns
      ) {
        throw new Error(
          `Invalid column ${move}. Columns must be between 0 and ${game.columns - 1}.`
        );
      }
    }
    if (!game.players || typeof game.players !== "object") {
      throw new Error("players must specify both players.");
    }
    if (
      typeof game.players["1"] !== "string" ||
      typeof game.players["2"] !== "string"
    ) {
      throw new Error("players must contain names for players 1 and 2.");
    }
    // Check that every move is physically possible.
    const heights = Array(game.columns).fill(0);
    for (const column of game.moves) {
      if (heights[column] >= game.rows) {
        throw new Error(`Column ${column} is full.`);
      }
      heights[column]++;
    }
  }
}

// Render the game at the current move
function renderBoard() {
  if (!game) return;

  const { rows, columns, moves, players, result, num_moves } = game;
  // Start with an empty board.
  const grid = Array.from(
    { length: rows },
    () => Array(columns).fill(0)
  );
  // Replay the first currentMove moves.
  for (let i = 0; i < currentMove; i++) {
    const col = moves[i];
    const player = (i % 2) + 1;
    // Find the lowest empty cell in this column.
    for (let row = rows - 1; row >= 0; row--) {
      if (grid[row][col] === 0) {
        grid[row][col] = player;
        break;
      }
    }
  }
  // Rebuild the visual board.
  board.innerHTML = "";
  board.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
  board.style.gridTemplateRows = `repeat(${rows}, 1fr)`;

  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < columns; col++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      if (grid[row][col] === 1) {
        cell.classList.add("red");
      } else if (grid[row][col] === 2) {
        cell.classList.add("yellow");
      }
      board.appendChild(cell);
    }
  }
  // Update game information.
  document.getElementById("player1Name").textContent = `${players["1"]} (${result === 1 ? "W" : (result == 0 ? "D" : "L")})`;
  document.getElementById("player2Name").textContent = `${players["2"]} (${result === -1 ? "W" : (result == 0 ? "D" : "L")})`;
  document.getElementById("gameNumber").textContent = `${games.findIndex(found => found === game) + 1} / ${games.length}`;
  
  
  document.getElementById("moveCount").textContent = `${currentMove} / ${num_moves}`;
  // Prevent navigation past either end.
  resetButton.disabled = (currentGame === 0 && currentMove === 0);
  backButton.disabled = (currentGame === 0 && currentMove === 0);
  nextButton.disabled = (currentGame === games.length - 1 && currentMove === num_moves);
  endButton.disabled = (currentGame === games.length - 1 && currentMove === num_moves);
}

function renderStats() {
  player1Wins = filteredGames.filter((game) => game["result"] == 1).length;
  player2Wins = filteredGames.filter((game) => game["result"] == -1).length;
  draws = filteredGames.filter((game) => game["result"] == 0).length;
  avgMoves = filteredGames.reduce((accum, curr) => accum + curr["num_moves"], 0) / filteredGames.length;

  stddev = Math.sqrt((filteredGames.reduce((accum, curr) => accum + (curr["num_moves"] - avgMoves) ** 2, 0) / (filteredGames.length - 1)));
  document.getElementById("decisiveXDraws").textContent = `${player1Wins + player2Wins} / ${draws}`;
  document.getElementById("avgMovesPerGame").textContent = `${avgMoves.toFixed(2)} / ${stddev.toFixed(2)}`;
  document.getElementById("player1WDL").textContent = `${player1Wins} / ${draws} / ${player2Wins}`
  document.getElementById("player2WDL").textContent = `${player2Wins} / ${draws} / ${player1Wins}`
}

function reset() {
  if (!filteredGames) return;
  if (currentMove !== 0) {
    currentMove = 0;
  } else if (currentGame === 0) {
    return;
  } else {
    currentGame--;
    game = filteredGames[currentGame];
    currentMove = game.moves.length;
  }
  renderBoard();
}

function back() {
  if (!game) return;
  currentMove = Math.max(0, currentMove - 1);
  renderBoard();
}

function next() {
  if (!game) return;
  currentMove = Math.min(game.moves.length, currentMove + 1);
  renderBoard();
}

function end() {
  if (!game) return;
  if (currentMove !== game.moves.length) {
    currentMove = game.moves.length;
  } else if (currentGame === filteredGames.length - 1) {
    return;
  } else {
    currentGame++;
    game = filteredGames[currentGame];
    currentMove = 0;
  }
  renderBoard();
}

// Playback controls
resetButton.addEventListener("click", () => reset());
backButton.addEventListener("click", () => back());
nextButton.addEventListener("click", () => next());
endButton.addEventListener("click", () => end());
window.addEventListener("keydown", (event) => {
  switch (event.key) {
    case "ArrowUp":
      end();
      break;
    case "ArrowDown":
      reset();
      break;
    case "ArrowLeft":
      back()
      break;
    case "ArrowRight":
      next()
      break;
    default:
      return;
  }
  // Prevent default scrolling behavior caused by arrow keys
  event.preventDefault(); 
});
