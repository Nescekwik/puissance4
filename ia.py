import math
import random
import time
from board import ROWS, COLS, N_ALIGN, PLAYER, OPPONENT, valid_moves, play_move, undo_move, WIN_PATTERNS, board_hash

MAX_DEPTH = 10

transposition_table = {}
killer_moves = {}

def check_win_fast(board, player):
    for pattern in WIN_PATTERNS:
        if all(board[r][c] == player for r, c in pattern):
            return True
    return False

def Terminal_Test(board):
    from board import is_full
    return check_win_fast(board, PLAYER) or check_win_fast(board, OPPONENT) or is_full(board)

def score_position_fast(board, player):
    if check_win_fast(board, player):
        return 1000
    if check_win_fast(board, -player):
        return -1000

    score = 0
    center = COLS // 2
    rows, cols, n = ROWS, COLS, N_ALIGN
    for r in range(rows):
        row = board[r]
        for c in range(cols):
            if row[c] == player:
                score += 3 - abs(c - center)

    directions = ((0,1), (1,0), (1,1), (1,-1))
    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                cnt_p = cnt_o = cnt_e = 0
                for i in range(n):
                    rr, cc = r + dr*i, c + dc*i
                    if not (0 <= rr < rows and 0 <= cc < cols):
                        break
                    cell = board[rr][cc]
                    if cell == player:
                        cnt_p += 1
                    elif cell == -player:
                        cnt_o += 1
                    else:
                        cnt_e += 1
                else:
                    if cnt_p > 0 and cnt_o == 0:
                        if cnt_p == 3:
                            score += 50
                        elif cnt_p == 2:
                            score += 10
                    elif cnt_o > 0 and cnt_p == 0:
                        if cnt_o == 3:
                            score -= 80
    return score

def minimax_cached(board, depth, alpha, beta, maximizing, start_time, time_limit=10):
    if (time.time() - start_time) > time_limit:
        return score_position_fast(board, PLAYER), None

    board_key = board_hash(board)
    if board_key in transposition_table:
        stored_depth, stored_eval, stored_move = transposition_table[board_key]
        if stored_depth >= depth:
            return stored_eval, stored_move

    if Terminal_Test(board) or depth == 0:
        eval_score = score_position_fast(board, PLAYER)
        transposition_table[board_key] = (depth, eval_score, None)
        return eval_score, None

    moves = valid_moves(board)
    if not moves:
        return score_position_fast(board, PLAYER), None

    center = COLS // 2
    killers = killer_moves.get(depth)
    if killers:
        moves.sort(key=lambda x: (x not in killers, abs(center-x)))
    else:
        moves.sort(key=lambda x: abs(center-x))

    if maximizing:
        max_eval = -math.inf
        best_col = moves[0]
        for col in moves:
            row = play_move(board, col, PLAYER)
            if row >= 0:
                eval_score, _ = minimax_cached(board, depth-1, alpha, beta, False, start_time, time_limit)
                undo_move(board, col, row)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_col = col
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    if depth not in killer_moves:
                        killer_moves[depth] = set()
                    killer_moves[depth].add(col)
                    break
        transposition_table[board_key] = (depth, max_eval, best_col)
        return max_eval, best_col
    else:
        min_eval = math.inf
        best_col = moves[0]
        for col in moves:
            row = play_move(board, col, OPPONENT)
            if row >= 0:
                eval_score, _ = minimax_cached(board, depth-1, alpha, beta, True, start_time, time_limit)
                undo_move(board, col, row)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_col = col
                beta = min(beta, eval_score)
                if beta <= alpha:
                    if depth not in killer_moves:
                        killer_moves[depth] = set()
                    killer_moves[depth].add(col)
                    break
        transposition_table[board_key] = (depth, min_eval, best_col)
        return min_eval, best_col

def IA_Decision(board):
    global transposition_table
    if len(transposition_table) > 100000:
        transposition_table.clear()
        killer_moves.clear()
    t0 = time.time()
    best_col = None
    TIME_LIMIT = 9.9
    for depth in range(1, MAX_DEPTH + 1):
        if (time.time() - t0) > TIME_LIMIT:
            break
        try:
            _, col = minimax_cached(board, depth, -math.inf, math.inf, True, t0, time_limit=TIME_LIMIT)
            if col is not None:
                best_col = col
            if (time.time() - t0) > TIME_LIMIT:
                break
        except:
            break
    if best_col is None:
        valid = valid_moves(board)
        return random.choice(valid) if valid else 0
    return best_col

def check_win(board, player):
    return check_win_fast(board, player)

def score_position(board, player):
    return score_position_fast(board, player)

def minimax(board, depth, alpha, beta, maximizing, start_time, time_limit=10):
    return minimax_cached(board, depth, alpha, beta, maximizing, start_time, time_limit)