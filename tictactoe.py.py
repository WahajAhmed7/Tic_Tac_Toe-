import math
import time

# Initialize empty board
board = [' ' for _ in range(9)]

def print_board():
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def available_moves():
    return [i for i, spot in enumerate(board) if spot == ' ']

def make_move(position, player):
    if board[position] == ' ':
        board[position] = player
        return True
    return False

def winner(player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_full():
    return ' ' not in board

# Minimax Algorithm
def minimax(is_maximizing):
    if winner('O'):
        return 1
    if winner('X'):
        return -1
    if is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves():
            board[move] = 'O'
            score = minimax(False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves():
            board[move] = 'X'
            score = minimax(True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

# Minimax with Alpha-Beta Pruning
def minimax_ab(is_maximizing, alpha, beta):
    if winner('O'):
        return 1
    if winner('X'):
        return -1
    if is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves():
            board[move] = 'O'
            score = minimax_ab(False, alpha, beta)
            board[move] = ' '
            best_score = max(score, best_score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in available_moves():
            board[move] = 'X'
            score = minimax_ab(True, alpha, beta)
            board[move] = ' '
            best_score = min(score, best_score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

def best_move(use_alpha_beta=False):
    best_score = -math.inf
    move = None
    for pos in available_moves():
        board[pos] = 'O'
        if use_alpha_beta:
            score = minimax_ab(False, -math.inf, math.inf)
        else:
            score = minimax(False)
        board[pos] = ' '
        if score > best_score:
            best_score = score
            move = pos
    return move

def play_game(use_alpha_beta=False):
    current_player = 'X'  # Human starts
    print_board()

    while True:
        if current_player == 'X':
            position = int(input("Enter your move (0-8): "))
            if make_move(position, 'X'):
                if winner('X'):
                    print_board()
                    print("You win!")
                    break
                current_player = 'O'
        else:
            print("AI is thinking...")
            start = time.time()
            position = best_move(use_alpha_beta)
            end = time.time()
            make_move(position, 'O')
            print(f"AI chose position {position} (time: {end-start:.4f} seconds)")
            if winner('O'):
                print_board()
                print("AI wins!")
                break
            current_player = 'X'
        
        print_board()

        if is_full():
            print("It's a draw!")
            break

if __name__ == "__main__":
    choice = input("Use Alpha-Beta Pruning? (y/n): ")
    use_ab = choice.lower() == 'y'
    play_game(use_ab)


