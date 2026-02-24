import math


board = [" " for _ in range(9)]


def print_board():
    for i in range(3):
        print(board[i*3] + " | " + board[i*3+1] + " | " + board[i*3+2])
        if i < 2:
            print("--+---+--")


def check_winner(player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],   
        [0,3,6], [1,4,7], [2,5,8],   
        [0,4,8], [2,4,6]             
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False


def is_draw():
    return " " not in board


def minimax(is_maximizing):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"


def human_move():
    while True:
        try:
            move = int(input("Enter position (1-9): ")) - 1
            if board[move] == " ":
                board[move] = "X"
                break
            else:
                print("Position already taken!")
        except:
            print("Invalid input!")


def play_game():
    print("Tic Tac Toe - You (X) vs AI (O)")
    print_board()

    while True:
        human_move()
        print_board()
        if check_winner("X"):
            print("You Win!")
            break
        if is_draw():
            print("It's a Draw!")
            break

        ai_move()
        print("AI Move:")
        print_board()
        if check_winner("O"):
            print("AI Wins!")
            break
        if is_draw():
            print("It's a Draw!")
            break

play_game()
