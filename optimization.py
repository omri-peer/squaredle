import random
import itertools
from tqdm import tqdm
from copy import deepcopy
import bisect

from squaredle import Squaredle, ENGLISH_LETTERS

def replace_letters(board, coords, scoring_func):
    n = len(coords)
    curr_letters = [board[i][j] for i,j in coords]
    max_score = 0
    best_letters = ["A" for _ in range(n)]
    for letters in itertools.product(ENGLISH_LETTERS, repeat=n):
        for k in range(n):
            i = coords[k][0]
            j = coords[k][1]
            board[i][j] = letters[k]
        score = scoring_func(board)
        if score > max_score:
            max_score = score
            best_letters = letters
    
    for k in range(n):
        i = coords[k][0]
        j = coords[k][1]
        board[i][j] = curr_letters[k]
    return best_letters, max_score

def nudge(board, scoring_func, num_squares=1, steps=1):
    for _ in range(steps):
        coords = [(random.randint(0, 3), random.randint(0, 3)) for k in range(num_squares)]
        best_letters, max_score = replace_letters(board, coords, scoring_func)
        for k in range(num_squares):
            i = coords[k][0]
            j = coords[k][1]
            board[i][j] = best_letters[k]
    return max_score

def gradient_step(board, scoring_func):
    max_score = 0
    best_i = 0
    best_j = 0
    best_letter = "A"
    for i in range(4):
        for j in range(4):
            letters, score = replace_letters(board, [(i,j)], scoring_func)
            letter = letters[0]
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

def nudge_all_the_way(board, scoring_func, num_squares=1):
    prev_score = -1
    score = scoring_func(board)
    while True:
        prev_score = score
        score = nudge(board, scoring_func, num_squares=num_squares, steps=100)
        print(score)
        if score > prev_score:
            continue

        gradient_step(board, scoring_func)
        score = scoring_func(board)
        if score == prev_score:
            return

def gradient_ascent(board, scoring_func):
    prev_score = -1
    score = scoring_func(board)
    while score > prev_score:
        prev_score = score
        score = gradient_step(board, scoring_func)
    return score

def nudge_grad_noise(board, scoring_func):
    pre_nudge_score = -1
    score = scoring_func(board)

    best_board = None
    max_score = -1
    regret_streak = 0
    while regret_streak <= 10:
        not_helping_streak = 0
        while not_helping_streak <= 10:
            pre_nudge_score = score
            score = nudge(board, scoring_func, steps=50)
            # print(f'NUDGE: {pre_nudge_score} -> {score}')
            not_helping_streak += 1

            if score == pre_nudge_score:
                pre_grad_score = score
                score = gradient_step(board, scoring_func)
                print(f'GRAD ({not_helping_streak}/10): {pre_grad_score} -> {score}')
            if score > pre_nudge_score:
                if score > max_score:
                    best_board = deepcopy(board)
                    max_score = score
                    not_helping_streak = 0
                    regret_streak = 0
                continue

            # print(f'STUCK: {score=}')
            pre_move_score = score
            add_noise(board, squares=1)
            score = scoring_func(board)
            # print(f'MOVED: {pre_move_score} -> {score}')
        
        for i in range(4):
            for j in range(4):
                board[i][j] = best_board[i][j]
        print(f'TELEP ({regret_streak}/10): {score} -> {max_score}')
        regret_streak += 1
        score = max_score

def grad_move_telep(board, scoring_func):
    regret_streak = 0
    best_board = None
    max_score = -1
    while regret_streak <= 10:
        move_streak = 0
        while move_streak <= 10:
            score = gradient_ascent(board, scoring_func)
            if score > max_score:
                best_board = deepcopy(board)
                max_score = score
                move_streak = 0
                regret_streak = 0
            else:
                move_streak += 1
                pre_move_score = score
                add_noise(board, squares=2)
                score = scoring_func(board)
                print(f'MOVED ({move_streak}/10): {pre_move_score} -> {score}')
        
        regret_streak += 1
        for i in range(4):
            for j in range(4):
                board[i][j] = best_board[i][j]
        print(f'TELEP ({regret_streak}/10): {score} -> {max_score}')

def grad_double_nudge(board, scoring_func):
    prev_score = -1
    score = scoring_func(board)
    while score > prev_score:
        prev_score = score
        score = nudge(board, scoring_func, 2, 5)
        print(f'NUDGE: {prev_score} -> {score}')
        score = gradient_ascent(board, scoring_func)
    return score

def grad_double_nudge_move_telep(board, scoring_func):
    regret_streak = 0
    best_board = None
    max_score = -1
    while regret_streak <= 10:
        move_streak = 0
        while move_streak <= 10:
            score = grad_double_nudge(board, scoring_func)
            if score > max_score:
                best_board = deepcopy(board)
                max_score = score
                move_streak = 0
                regret_streak = 0
            else:
                move_streak += 1
                pre_move_score = score
                add_noise(board, squares=2)
                score = scoring_func(board)
                print(f'MOVED ({move_streak}/10): {pre_move_score} -> {score}')
        
        regret_streak += 1
        for i in range(4):
            for j in range(4):
                board[i][j] = best_board[i][j]
        print(f'TELEP ({regret_streak}/10): {score} -> {max_score}')

def follow_favorites(board, scoring_func):
    squaredle = Squaredle() # REMOVE!!!
    favorites = []
    done = []
    done_scores = set([])
    
    score = grad_double_nudge(board, scoring_func)
    best_board = deepcopy(board)
    max_score = score

    bisect.insort(favorites, (score, deepcopy(board)))
    while favorites:
        score, board = favorites.pop(-1)
        bisect.insort(done, (score, deepcopy(board)))
        done_scores.add(score)
        for _ in range(5):
            child = deepcopy(board)
            add_noise(child, squares=2)
            score = grad_double_nudge(child, scoring_func)
            if score > max_score:
                best_board = deepcopy(child)
                max_score = score
                squaredle.print_board(best_board)

            already_done = False
            if score in done_scores:
                for done_score, done_board in done: # Inefficient!!!
                    if done_score == score:
                        if all(all(done_board[i][j] == child[i][j] for j in range(4)) for i in range(4)):
                            already_done = True
                            break
            
            if not already_done:
                bisect.insort(favorites, (score, child))
                if len(favorites) >= 10:
                    favorites.pop(0)

        print(f'favorites: {[score for score, _ in favorites]}')
        print(f'best: {max_score}')


            