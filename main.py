from tqdm import tqdm
import numpy as np
from matplotlib import pyplot as plt

from utils import *
from squaredle import Squaredle
from optimization import *

BOARD = """
O R E S
S T I L
E N A P
G R E S
"""

def main():
    squaredle = Squaredle()
    board = load_board(BOARD)
    squaredle.print_board(board)
    follow_favorites(board, scoring_func=squaredle.get_score)
    squaredle.print_board(board)

if __name__ == '__main__':
  main()