from board import create_board, print_board, play_move, PLAYER, OPPONENT
from ia import IA_Decision, Terminal_Test, check_win

def simulate_games(n=10):
    p1_wins, p2_wins, draws = 0, 0, 0
    for i in range(n):
        board = create_board()
        turn = PLAYER
        while not Terminal_Test(board):
            col = IA_Decision(board)
            play_move(board, col, turn)
            turn *= -1
        if check_win(board, PLAYER):
            p1_wins += 1
        elif check_win(board, OPPONENT):
            p2_wins += 1
        else:
            draws += 1
    print(f"Sur {n} parties : IA1 gagne {p1_wins} fois, IA2 gagne {p2_wins} fois, {draws} nuls.")

if __name__ == "__main__":
    simulate_games(5)