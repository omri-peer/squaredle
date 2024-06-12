from tqdm import tqdm
import numpy as np
from matplotlib import pyplot as plt
from squaredle import Squaredle
from optimization import *

def main():
    squaredle = Squaredle()
    board = squaredle.create_board()
    squaredle.print_board(board)
    follow_favorites(board, scoring_func=squaredle.get_score)
    squaredle.print_board(board)

if __name__ == '__main__':
  main()