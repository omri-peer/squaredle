import os
from letter_frequency import get_letter, get_stupid_letter
import random
from tqdm import tqdm

YESTERDAY_BOARD = [['A', 'B', 'U', 'S'],['N', 'O', 'T', 'P'],['W', 'R', 'M', 'U'],['R', 'A', 'E', 'N']]
BOARD = [['P', 'N', 'V', 'T'],['H', 'I', 'O', 'Y'],['T', 'V', 'L', 'B'],['D', 'I', 'O', 'B']]
ENGLISH_LETTERS = list(map(chr, range(ord('A'), ord('Z')+1)))
words_tree = { }

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

def words_with_prefix(board, p, last_dict, last, remaining):
    words = []
    if " " in last_dict:
        words.append(p)

    for i in range(last[0] - 1, last[0] + 2):
        for j in range(last[1] - 1, last[1] + 2):
            if ([i,j] in remaining) and (board[i][j] in last_dict):
                remaining.remove([i, j])
                more_words = words_with_prefix(board, p + board[i][j], last_dict[board[i][j]], [i, j], remaining)
                remaining.append([i, j])
                words.extend(more_words)

    return words

def get_words(board, verbose=False):
    all_words = []
    remain = [[i, j] for i in range(4) for j in range(4)]
    for i in range(4):
        for j in range(4):
            remain.remove([i,j])
            all_words.extend(words_with_prefix(board, board[i][j], words_tree[board[i][j]], [i,j], remain))
            remain.append([i, j])
    all_words = list(set(all_words))

    if verbose:
        print(all_words)
        print(len(all_words))

    return all_words

def print_board(board):
    print("\n".join([" ".join(row) for row in board]))
    print(get_score(board))
    print(get_words(board))

def get_stupid_board():
    return [[get_letter() for i in range(4)] for j in range(4)]


def get_score(board):
    return len(get_words(board))

def nudge(board, scoring_func=get_score):
    i = random.randint(0, 3)
    j = random.randint(0, 3)
    max_score = 0
    best_letter = "A"
    for letter in ENGLISH_LETTERS:
        board[i][j] = letter
        score = scoring_func(board)
        if score > max_score:
            max_score = score
            best_letter = letter
    board[i][j] = best_letter

words_tree = create_tree()
print("Created tree")
board = get_stupid_board()
print_board(board)
for _ in tqdm(range(10000)):
    nudge(board)

print_board(board)
