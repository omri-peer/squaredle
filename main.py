from squaredle import Squaredle
from optimization import *

def main():
    squaredle = Squaredle()
    board = squaredle.create_board()
    squaredle.print_board(board)
    nudge_grad_noise(board, scoring_func=squaredle.get_score)
    squaredle.print_board(board)

if __name__ == '__main__':
  main()