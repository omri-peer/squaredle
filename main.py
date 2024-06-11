from squaredle import Squaredle
from optimization import *

def main():
    squaredle = Squaredle()
    board = squaredle.create_board()
    squaredle.print_board(board)
    grad_double_nudge_move_telep(board, scoring_func=squaredle.get_score)
    squaredle.print_board(board)

if __name__ == '__main__':
  main()