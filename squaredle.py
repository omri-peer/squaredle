import os
import random
from tqdm import tqdm

YESTERDAY_BOARD = [['A', 'B', 'U', 'S'],['N', 'O', 'T', 'P'],['W', 'R', 'M', 'U'],['R', 'A', 'E', 'N']]
BOARD = [['P', 'N', 'V', 'T'],['H', 'I', 'O', 'Y'],['T', 'V', 'L', 'B'],['D', 'I', 'O', 'B']]
ENGLISH_LETTERS = list(map(chr, range(ord('A'), ord('Z')+1)))

def create_tree():
    f = open("NWL2023.txt")
    words_tree = { }
    for i, line in enumerate(f):
        word = line.split(" ")[0]
        if len(word) < 4:
            continue
        curr_dict = words_tree
        for letter in word:
            if letter not in curr_dict:
                curr_dict[letter] = { }
            curr_dict = curr_dict[letter]
        # mark end of word
        curr_dict[" "] = {}

    f.close()
    return words_tree

class Squaredle:
    def __init__(self) -> None:
        self.words_tree = create_tree()

    def words_with_prefix(self, board, p, last_dict, last, current, words=[], usage=None):
        if " " in last_dict:
            if usage is not None:
                if p not in words:
                    for (i0, j0) in current:
                        usage[i0][j0] += 1
            words.add(p)

        for i in range(max(last[0] - 1, 0), min(last[0] + 2, 4)):
            for j in range(max(last[1] - 1, 0), min(last[1] + 2, 4)):
                if ((i, j) not in current) and (board[i][j] in last_dict):
                    current.add((i, j))
                    self.words_with_prefix(board, p + board[i][j], last_dict[board[i][j]], (i, j), current, words, usage)
                    current.remove((i, j))

    def get_words(self, board, with_usage=False, verbose=False):
        all_words = set([])
        current = set([])
        if with_usage:
            all_usage = [[0 for _ in range(4)] for __ in range(4)]
        else:
            all_usage = None
        for i in range(4):
            for j in range(4):
                current.add((i, j))
                self.words_with_prefix(board, board[i][j], self.words_tree[board[i][j]], [i,j], current, all_words, all_usage)
                current.remove((i, j))

        if verbose:
            print(sorted(list(all_words)))
            print(len(all_words))

        return all_words, all_usage

    def print_board(self, board):
        print("\n".join([" ".join(row) for row in board]))
        print(self.get_score(board))
        # print(self.get_words(board))

    def get_score(self, board):
        return len(self.get_words(board)[0])
