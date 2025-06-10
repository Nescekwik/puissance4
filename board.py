ROWS = 6
COLS = 12
N_ALIGN = 4
EMPTY = 0
PLAYER = 1
OPPONENT = -1

WIN_PATTERNS = ()
def _init_win_patterns():
    global WIN_PATTERNS
    if WIN_PATTERNS:
        return
    patterns = []
    rows, cols, n = ROWS, COLS, N_ALIGN
    for r in range(rows):
        for c in range(cols-n+1):
            patterns.append(tuple((r, c+i) for i in range(n)))
    for c in range(cols):
        for r in range(rows-n+1):
            patterns.append(tuple((r+i, c) for i in range(n)))
    for r in range(n-1, rows):
        for c in range(cols-n+1):
            patterns.append(tuple((r-i, c+i) for i in range(n)))
    for r in range(rows-n+1):
        for c in range(cols-n+1):
            patterns.append(tuple((r+i, c+i) for i in range(n)))
    WIN_PATTERNS = tuple(patterns)

_init_win_patterns()

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("\n".join(["| " + " ".join(["X" if cell==1 else "O" if cell==-1 else "." for cell in row]) for row in board]))
    print("-" * (2*COLS+1))
    print("  " + " ".join([str(c) for c in range(COLS)]))

def valid_moves(board):
    top_row = board[0]
    return [c for c in range(COLS) if top_row[c] == EMPTY]

def play_move(board, col, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return row
    return -1

def undo_move(board, col, row=None):
    if row is not None:
        board[row][col] = EMPTY
    else:
        for row in range(ROWS):
            if board[row][col] != EMPTY:
                board[row][col] = EMPTY
                return

def is_full(board):
    return not any(cell == EMPTY for cell in board[0])

def board_hash(board):
    h = 0
    rows, cols = ROWS, COLS
    for r in range(rows):
        row = board[r]
        for c in range(cols):
            h = h * 3 + (row[c] + 1)
    return h