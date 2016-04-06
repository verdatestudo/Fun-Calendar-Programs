'''
Knights Tour using Warnsdorff's Rule

Description:
A Knight's Tour is visiting every square on a board once.
Wansdorff's Rule is a heuristic for achieving this, by always choosing the square with
the fewest number of possible onward moves.

First Created: 2016-Apr-06
Last Updated: 2016-Apr-06
Python 2.7
Chris
'''


def find_possible_moves(current_square_x, current_square_y, grid_size, board):
    '''
    Find all possible moves from the knights current position
    Return a list of possible moves and the number of possible moves
    '''

    # all possible knight moves
    knight_moves = [[current_square_x - 2, current_square_y + 1], [current_square_x - 2, current_square_y - 1], \
    [current_square_x + 2, current_square_y + 1], [current_square_x + 2, current_square_y - 1],\
    [current_square_x - 1, current_square_y + 2], [current_square_x - 1, current_square_y - 2],\
    [current_square_x + 1, current_square_y + 2], [current_square_x + 1, current_square_y - 2]]

    possible_moves = []

    # if knight move is in board range (0-->grid_size) and it hasn't been visited already
    for item in knight_moves:
        if item[0] in range(grid_size) and item[1] in range(grid_size) and board[item[0]][item[1]] == 0:
            possible_moves.append(item)

    return possible_moves, len(possible_moves)

def count_possible_moves(possible_move_list, grid_size, board):
    '''
    Takes the possible move list from find_possible_moves and checks which
    has the fewest onwards moves
    '''

    fewest_count = float('inf')

    for item in possible_move_list:
        new_moves = find_possible_moves(item[0], item[1], grid_size, board)
        # if move has fewer onwards moves than current best (but more than zero)
        if new_moves[1] < fewest_count and new_moves[1] > 0:
            fewest_count = new_moves[1]
            best_move = item

    # if we can't find any onwards moves, then we just need to move to the Last
    # remaining square and finish.
    if fewest_count == float('inf'):
        best_move = possible_move_list[0]
        move_knight(best_move, board)
        return None

    # make the move and then start the process again
    move_knight(best_move, board)
    return count_possible_moves(find_possible_moves(best_move[0], best_move[1], grid_size, board)[0], grid_size, board)

def move_knight(best_move, board):
    '''
    Move the knight and update the counter
    '''
    global MOVE_COUNTER
    board[best_move[0]][best_move[1]] = MOVE_COUNTER
    MOVE_COUNTER += 1

def print_board(title, board):
    '''
    Prints the current state of the board along with a title message
    '''
    print '*** %s ***' %(title)
    for row in board:
        print row
    print '*** %s ***' %(title), '\n'

# default variables
MOVE_COUNTER = 1
SET_GRID_SIZE = 8
STARTING_SQUARE = [0, 0]
MY_BOARD = [[0] * SET_GRID_SIZE for i in range(SET_GRID_SIZE)]

# move the knight, print the board, get the process started
move_knight(STARTING_SQUARE, MY_BOARD)
print_board('Starting Board', MY_BOARD)
count_possible_moves(find_possible_moves(STARTING_SQUARE[0], STARTING_SQUARE[1], SET_GRID_SIZE, MY_BOARD)[0], SET_GRID_SIZE, MY_BOARD)
print_board('Final Board', MY_BOARD)
