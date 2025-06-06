ROWS = 6
COLS = 12
N_ALIGN = 4
EMPTY = 0
PLAYER = 1
OPPONENT = -1

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("\n".join(["| " + " ".join(["X" if cell==1 else "O" if cell==-1 else "." for cell in row]) for row in board]))
    print("-" * (2*COLS+1))
    print("  " + " ".join([str(c) for c in range(COLS)]))

def valid_moves(board):
    return [c for c in range(COLS) if board[0][c] == EMPTY]

def play_move(board, col, player):
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return True
    return False

def undo_move(board, col):
    for row in range(ROWS):
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            return

def is_full(board):
    return all(board[0][c] != EMPTY for c in range(COLS))