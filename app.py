from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)

# ❗ IMPORTANT: no eventlet → no warning
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

board = [""] * 9
players = []
player_symbols = {}

current_turn = "X"

WINS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]


@app.route("/")
def index():
    return render_template("index.html")


# ---------------- CONNECT ----------------
@socketio.on("connect")
def handle_connect():
    global players, player_symbols

    if len(players) >= 2:
        emit("full")
        return

    sid = request.sid
    players.append(sid)

    symbol = "X" if len(players) == 1 else "O"
    player_symbols[sid] = symbol

    emit("player", {"symbol": symbol})

    emit("board", {
        "board": board,
        "turn": current_turn,
        "winner": None
    }, broadcast=True)


# ---------------- MOVE ----------------
@socketio.on("move")
def handle_move(data):
    global board, current_turn

    sid = request.sid
    index = data.get("index")

    if sid not in player_symbols:
        return

    symbol = player_symbols[sid]

    # validate move
    if index is None or index < 0 or index > 8:
        return

    if board[index] != "" or symbol != current_turn:
        return

    # apply move
    board[index] = symbol
    winner = check_winner()

    # switch turn only if game continues
    if not winner:
        current_turn = "O" if current_turn == "X" else "X"

    emit("board", {
        "board": board,
        "turn": current_turn,
        "winner": winner
    }, broadcast=True)


# ---------------- WIN CHECK ----------------
def check_winner():
    for a, b, c in WINS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "DRAW"

    return None


# ---------------- RESET (optional but useful) ----------------
@socketio.on("reset")
def reset():
    global board, current_turn

    board = [""] * 9
    current_turn = "X"

    emit("board", {
        "board": board,
        "turn": current_turn,
        "winner": None
    }, broadcast=True)


# ---------------- DISCONNECT ----------------
@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid

    if sid in players:
        players.remove(sid)

    if sid in player_symbols:
        del player_symbols[sid]


# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)