from squaredle import Squaredle
from optimization import nudge_all_the_way

def main():
    squaredle = Squaredle()
    board = squaredle.get_board()
    squaredle.print_board(board)
    nudge_all_the_way(board, scoring_func=squaredle.get_score)
    squaredle.print_board(board)

if __name__ == '__main__':
  main()