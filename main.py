from board import create_board, print_board, valid_moves, play_move, ROWS, COLS, N_ALIGN, PLAYER, OPPONENT
from ia import IA_Decision, Terminal_Test, check_win

def human_vs_ia():
    board = create_board()
    print_board(board)
    first = input("Qui commence ? (h=humain, i=IA): ").strip().lower()
    turn = PLAYER if first=="i" else OPPONENT
    while not Terminal_Test(board):
        if turn == PLAYER:
            print("\nTour de l'IA...")
            col = IA_Decision(board)
            print(f"L'IA joue la colonne {col}")
        else:
            print("\nVotre tour.")
            valid = valid_moves(board)
            col = -1
            while col not in valid:
                try:
                    col = int(input(f"Colonne ? ({', '.join(map(str,valid))}) : "))
                except:
                    col = -1
        play_move(board, col, turn)
        print_board(board)
        turn *= -1

    if check_win(board, PLAYER):
        print("L'IA gagne !")
    elif check_win(board, OPPONENT):
        print("Bravo, vous gagnez !")
    else:
        print("Match nul !")

def ia_vs_ia():
    board = create_board()
    print_board(board)
    turn = PLAYER
    while not Terminal_Test(board):
        col = IA_Decision(board)
        play_move(board, col, turn)
        print(f"Joueur {'IA1' if turn==PLAYER else 'IA2'} joue colonne {col}")
        print_board(board)
        turn *= -1
    if check_win(board, PLAYER):
        print("IA1 gagne !")
    elif check_win(board, OPPONENT):
        print("IA2 gagne !")
    else:
        print("Match nul !")

# Pour tester :
if __name__ == "__main__":
    #human_vs_ia()
    ia_vs_ia()