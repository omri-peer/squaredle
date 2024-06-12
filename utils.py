from letter_frequency import get_letter

def create_board():
    return [[get_letter() for i in range(4)] for j in range(4)]

def load_board(board_str):
    return [row.split(' ') for row in board_str.split('\n')[1:-1]]