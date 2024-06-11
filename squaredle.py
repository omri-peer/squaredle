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

def get_board():
    return [[get_letter() for i in range(4)] for j in range(4)]

def get_score(board):
    return len(get_words(board))

def replace_letter(board, i, j, scoring_func):
    curr_letter = board[i][j]
    max_score = 0
    best_letter = "A"
    for letter in ENGLISH_LETTERS:
        board[i][j] = letter
        score = scoring_func(board)
        if score > max_score:
            max_score = score
            best_letter = letter
    board[i][j] = curr_letter
    return best_letter, max_score

def nudge(board, scoring_func=get_score, steps=1):
    for _ in range(steps):
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        best_letter, max_score = replace_letter(board, i, j, scoring_func)
        board[i][j] = best_letter
        return max_score

def gradient_step(board, scoring_func=get_score):
    max_score = 0
    best_i = 0
    best_j = 0
    best_letter = "A"
    for i in range(4):
        for j in range(4):
            letter, score = replace_letter(board, i, j, scoring_func)
            if score > max_score:
                best_i = i
                best_j = j
                best_letter = letter
                max_score = score
    board[best_i][best_j] = best_letter
    return max_score

def add_noise(board, squares=1):
    for i in range(squares):
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        letter = random.choice(ENGLISH_LETTERS)
        board[i][j] = letter

def nudge_all_the_way(board, scoring_func=get_score):
    prev_score = -1
    score = scoring_func(board)
    while True:
        prev_score = score
        score = nudge(board, scoring_func, steps=30)
        if score > prev_score:
            continue

        gradient_step(board, scoring_func)
        score = scoring_func(board)
        if score == prev_score:
            return


def nudge_noise_grad(board, scoring_func=get_score):
    pre_noise_score = -1
    pre_nudge_score = -1
    score = scoring_func(board)
    while score > pre_noise_score:
        while score > pre_nudge_score:
            pre_nudge_score = score
            score = nudge(board, scoring_func, steps=30)
            print(score)
        print(f'STUCK, {score=}')
        pre_noise_score = score
        add_noise(board, squares=5)
        for i in range(5):
            score = gradient_step(board, scoring_func)
        print(f'MOVED, {score=}')

words_tree = create_tree()
board = get_board()
print_board(board)
nudge_all_the_way(board, scoring_func=get_score)
print_board(board)
