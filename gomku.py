"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""


def is_empty(board):
    if board == make_empty_board(len(board)):
        return True
    return False

##Is bounded
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''
        returns whether a sequence of a particular length is open, semi-open or closed
    '''

    start_closed = False
    end_closed = False

    x_start = x_end - d_x * (length - 1)
    y_start = y_end - d_y * (length - 1)

    #this means that the sequence is vertical
    if d_y == 1 and d_x == 0:
        if y_start == 0 or board[y_start - 1][x_end] != " ":
            start_closed = True
        if y_end == len(board) - 1 or board[y_end + 1][x_end] != " ":
            end_closed = True

    #this means that the sequence is horizontal
    elif d_y == 0 and d_x == 1:
        if x_start == 0 or board[y_end][x_start - 1] != " ":
            start_closed = True
        if x_end == len(board) - 1 or board[y_end][x_end + 1] != " ":
            end_closed = True

    #this means that the sequence is diagonal with negative slope
    elif d_y == 1 and d_x == 1:
        if (y_start or x_start) == 0 or board[y_start - 1][x_start - 1] != " ":
            start_closed = True
        if y_end == len(board) - 1 or x_end == len(board) - 1 or board[y_end + 1][x_end + 1] != " ":
            end_closed = True

    #else sequence must be diagonal with negative slope
    else:
        if y_start == 0 or x_start == len(board) - 1 or board[y_start - 1][x_start + 1] != " ":
            start_closed = True
        if y_end == len(board) - 1 or x_end == 0 or board[y_end + 1][x_end - 1] != " ":
            end_closed = True

    #final return statements
    if start_closed and end_closed:
        return "CLOSED"
    elif start_closed or end_closed:
        return "SEMIOPEN"
    else:
        return "OPEN"


##DETECT ROW
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    '''
    returns the number of sequences of a given length and colour a ROW
    assumes y_start and x_start are at the begining of the row
    '''

    #finds all squares in row that contains the desired colour
    squares_with_col = find_sqrs_of_col(board, col, y_start, x_start, d_y, d_x)

    #finds how long each sequence is and what its last coordinate is
    temp_seq_ends, sequence_lengths = len_seq_and_end_coor(squares_with_col, d_y, d_x)

    #eliminates any sequences not of specified length
    sequence_ends = find_propre_length(temp_seq_ends, sequence_lengths, length)

    #determines the boundings on each seqence
    open_seq_count, semi_open_seq_count, closed_seq_count = bounding_of_row(board, sequence_ends, length, d_y, d_x)

    return open_seq_count, semi_open_seq_count




def find_sqrs_of_col(board, col, y_start, x_start, d_y, d_x):
    '''
    finds all squares in row that contains the desired colour
    '''
    squares_with_col = []
    y = y_start
    x = x_start

    for i in range(max_length(board, y_start, x_start, d_y, d_x)):
        if board[y][x] == col:
            squares_with_col.append([y, x])
        y += d_y
        x += d_x
    return squares_with_col

def len_seq_and_end_coor(squares_with_col, d_y, d_x):
    '''
    finds how long each sequence is and what its last coordinate is
    '''
    sequence_lengths = []
    temp_seq_ends = []
    count = 1

    if len(squares_with_col) != 0:
        previous_tuple = squares_with_col[0]

        for i in range(1, len(squares_with_col)):
            predicted_previous_tuple = [squares_with_col[i][0] - d_y, squares_with_col[i][1] - d_x]
            if previous_tuple != predicted_previous_tuple:
                temp_seq_ends.append(previous_tuple)
                sequence_lengths.append(count)
                count = 1
            else:
                count += 1
            previous_tuple = squares_with_col[i]

        temp_seq_ends.append(squares_with_col[-1])
        sequence_lengths.append(count)
    return temp_seq_ends, sequence_lengths

def find_propre_length(temp_seq_ends, sequence_lengths, length):
    sequence_ends = []

    for i in range(len(sequence_lengths)):
        if sequence_lengths[i] == length:
            sequence_ends.append(temp_seq_ends[i])
    return sequence_ends

def bounding_of_row(board, sequence_ends, length, d_y, d_x):
    ''' determines the boundings on each seqence
    '''
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0

    for end in sequence_ends:
        returned_string = is_bounded(board, end[0], end[1], length, d_y, d_x)
        if returned_string == "OPEN":
            open_seq_count += 1
        elif returned_string == "SEMIOPEN":
            semi_open_seq_count += 1
        else:
            closed_seq_count += 1

    return open_seq_count, semi_open_seq_count, closed_seq_count

def max_length(board, y_start, x_start, d_y, d_x):
    '''
    assumes that y_start, x_start are at start of ROW
    '''
    if d_y == 0 or d_x == 0:
        return len(board)

    elif d_x == -1:
        if y_start > 0:
            return len(board) - y_start
        else:
           return x_start + 1

    else:
        if y_start > 0:
            return len(board) - y_start
        else:
            return len(board) - x_start


##DETECT ROWS
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0

    #check all rows
    for i in range(len(board)):
        tuple = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += tuple[0]
        semi_open_seq_count += tuple[1]
        #print(tuple)

    #check all columns
    for i in range(len(board)):
        #print("column", i)
        tuple = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += tuple[0]
        semi_open_seq_count += tuple[1]
        #print(tuple)

    #check all diagonals with -ve slope
    for i in range(len(board)):
        #print("-ve diagonal", i)
        if i != 0:
            horizontal_start = detect_row(board, col, 0, i, length, 1, 1)
            open_seq_count += horizontal_start[0]
            semi_open_seq_count += horizontal_start[1]
            #print(horizontal_start)

        vertical_start = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += vertical_start[0]
        semi_open_seq_count += vertical_start[1]
        #print(vertical_start)

    #check all diagonals with +ve slope
    for i in range(len(board)):
        #print("+ve diagonal", i)

        if i != len(board) - 1:
            horizontal_start = detect_row(board, col, 0, i, length, 1, -1)
            open_seq_count += horizontal_start[0]
            semi_open_seq_count += horizontal_start[1]
            #print(horizontal_start)

        vertical_start = detect_row(board, col, i, len(board) - 1, length, 1, -1)
        open_seq_count += vertical_start[0]
        semi_open_seq_count += vertical_start[1]
        #print(vertical_start)

    return open_seq_count, semi_open_seq_count

##SEARCH MAX
def search_max(board):
    ''' finds the location (y, x) such that (y, x) is empty and putting a black stone on (y, x) maximizes the score of the board as calculated by score()
    if their are multiple tuples you can use, it only chooses one
    DOES NOT MUTATE BOARD
    '''

    scoring_board = make_empty_board(len(board))

    #see how much you would score in each spot
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == " ":
                board[y][x] = "b"
                scoring_board[y][x] = score(board)
                board[y][x] = " "
    print_board(scoring_board)

    #determine the spot(s) where you earn the highest scores

    max_score = -100000
    max_score_coor = []

    for y in range(len(board)):
        for x in range(len(board)):
            if scoring_board[x][y] != " " and scoring_board[x][y] > max_score:
                max_score = scoring_board[x][y]
                max_score_coor = [[x, y]]
            elif scoring_board[x][y] != " " and scoring_board[x][y] == max_score:
                max_score_coor.append([x, y])
    print(max_score, max_score_coor)

    #chooses move_y and move_x, including a random case for instances where multiple spots will give the same score
    from random import randint

    if len(max_score_coor) == 0:
        move_y = randint(1, len(board)) - 1
        move_x = randint(1, len(board)) - 1
        if board[move_y][move_x] != " ":
            while board[move_y][move_x] != " ":
                move_y = randint(1, len(board)) - 1
                move_x = randint(1, len(board)) - 1

    else:
        random = randint(1, len(max_score_coor)) - 1
        move_y, move_x = max_score_coor[random]

    return move_y, move_x

##IS WIN
def is_win(board):

    if check_win(board) == "Black won":
        return "Black won"
    elif check_win(board) == "White won":
        return "White won"
    elif board_is_full(board):
        return "Draw"
    else:
        return "Continue playing!"



def board_is_full(board):
    for y in range(len(board)):
       for x in range(len(board)):
           if board[y][x] == " ":
               return False
    return True

def check_win(board):
    open_seq_count, semi_open_seq_count, closed_open_seq_count = 0, 0, 0
    col_list = ["b", "w"]

    for col in col_list:
        open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0

        #check all rows
        for i in range(len(board)):
            tuple = detect_row_with_closed(board, col, i, 0, 5, 0, 1)
            open_seq_count += tuple[0]
            semi_open_seq_count += tuple[1]
            closed_seq_count += tuple[2]

        #check all columns
        for i in range(len(board)):
            tuple = detect_row_with_closed(board, col, 0, i, 5, 1, 0)
            open_seq_count += tuple[0]
            semi_open_seq_count += tuple[1]
            closed_seq_count += tuple[2]

        #check pos slopes
        for i in range(len(board)):
            #print("+ve diagonal", i)

            if i != len(board) - 1:
                horizontal_start = detect_row_with_closed(board, col, 0, i, 5, 1, -1)
                open_seq_count += horizontal_start[0]
                semi_open_seq_count += horizontal_start[1]
                closed_seq_count += horizontal_start[2]

            vertical_start = detect_row_with_closed(board, col, i, len(board) - 1, 5, 1, -1)
            open_seq_count += vertical_start[0]
            semi_open_seq_count += vertical_start[1]
            closed_open_seq_count += vertical_start[2]

        #check neg slopes
        for i in range(len(board)):
            #print("-ve diagonal", i)
            if i != 0:
                horizontal_start = detect_row_with_closed(board, col, 0, i, 5, 1, 1)
                open_seq_count += horizontal_start[0]
                semi_open_seq_count += horizontal_start[1]
                closed_seq_count += horizontal_start[2]

            vertical_start = detect_row_with_closed(board, col, i, 0, 5, 1, 1)
            open_seq_count += vertical_start[0]
            semi_open_seq_count += vertical_start[1]
            closed_open_seq_count += vertical_start[2]

        #did the colour win?
        if open_seq_count > 0 or semi_open_seq_count > 0 or closed_seq_count > 0:
            if col == "b":
                return "Black won"
            else:
                return "White won"

def detect_row_with_closed(board, col, y_start, x_start, length, d_y, d_x):
    #finds all squares in row that contains the desired colour
    squares_with_col = find_sqrs_of_col(board, col, y_start, x_start, d_y, d_x)

    #finds how long each sequence is and what its last coordinate is
    temp_seq_ends, sequence_lengths = len_seq_and_end_coor(squares_with_col, d_y, d_x)

    #eliminates any sequences not of specified length
    sequence_ends = find_propre_length(temp_seq_ends, sequence_lengths, length)

    #determines the boundings on each seqence
    open_seq_count, semi_open_seq_count, closed_seq_count = bounding_of_row(board, sequence_ends, length, d_y, d_x)

    return open_seq_count, semi_open_seq_count, closed_seq_count

##DO NOT CHANGE ME
def score(board):
    '''
    depends on detect_rows()
    '''
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #