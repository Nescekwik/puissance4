import math
import random
import time
from board import ROWS, COLS, N_ALIGN, PLAYER, OPPONENT, valid_moves, play_move, undo_move

MAX_DEPTH = 5

def check_win(board, player):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS-N_ALIGN+1):
            if all(board[r][c+i]==player for i in range(N_ALIGN)):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS-N_ALIGN+1):
            if all(board[r+i][c]==player for i in range(N_ALIGN)):
                return True
    # Diagonal /
    for r in range(N_ALIGN-1, ROWS):
        for c in range(COLS-N_ALIGN+1):
            if all(board[r-i][c+i]==player for i in range(N_ALIGN)):
                return True
    # Diagonal \
    for r in range(ROWS-N_ALIGN+1):
        for c in range(COLS-N_ALIGN+1):
            if all(board[r+i][c+i]==player for i in range(N_ALIGN)):
                return True
    return False

def Terminal_Test(board):
    from board import is_full
    return check_win(board, PLAYER) or check_win(board, OPPONENT) or is_full(board)

def score_position(board, player):
    if check_win(board, player):
        return 1000
    if check_win(board, -player):
        return -1000
    score = 0
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in [(0,1),(1,0),(1,1),(1,-1)]:
                group = []
                for i in range(N_ALIGN):
                    rr = r + dr*i
                    cc = c + dc*i
                    if 0<=rr<ROWS and 0<=cc<COLS:
                        group.append(board[rr][cc])
                if len(group)==N_ALIGN:
                    cnt = group.count(player)
                    cnt_opp = group.count(-player)
                    if cnt == 3 and cnt_opp == 0:
                        score += 5
                    elif cnt == 2 and cnt_opp == 0:
                        score += 2
                    if cnt_opp == 3 and cnt == 0:
                        score -= 6
    return score

def minimax(board, depth, alpha, beta, maximizing, start_time, time_limit=10):
    if Terminal_Test(board) or depth == 0 or (time.time() - start_time) > time_limit:
        return score_position(board, PLAYER), None
    moves = valid_moves(board)
    random.shuffle(moves)
    if maximizing:
        max_eval = -math.inf
        best_col = moves[0]
        for col in moves:
            play_move(board, col, PLAYER)
            eval, _ = minimax(board, depth-1, alpha, beta, False, start_time, time_limit)
            undo_move(board, col)
            if eval > max_eval:
                max_eval = eval
                best_col = col
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_col
    else:
        min_eval = math.inf
        best_col = moves[0]
        for col in moves:
            play_move(board, col, OPPONENT)
            eval, _ = minimax(board, depth-1, alpha, beta, True, start_time, time_limit)
            undo_move(board, col)
            if eval < min_eval:
                min_eval = eval
                best_col = col
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_col

def IA_Decision(board):
    t0 = time.time()
    _, col = minimax([row[:] for row in board], MAX_DEPTH, -math.inf, math.inf, True, t0, time_limit=10)
    from board import valid_moves
    if col is None:
        valid = valid_moves(board)
        return random.choice(valid) if valid else 0
    return col