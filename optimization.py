import random
from squaredle import ENGLISH_LETTERS

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

def nudge(board, scoring_func, steps=1):
    for _ in range(steps):
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        best_letter, max_score = replace_letter(board, i, j, scoring_func)
        board[i][j] = best_letter
        return max_score

def gradient_step(board, scoring_func):
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

def nudge_all_the_way(board, scoring_func):
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

def nudge_noise_grad(board, scoring_func):
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