#!/usr/bin/env python3

from itertools import chain


def rows_to_cols(board):
    for i in range(len(board[0])):
        yield set(line[i] for line in board)


def load_input(filename):
    with open(filename) as input_file:
        boards = []
        balls = [int(ball) for ball in next(input_file).strip().split(",")]
        this_board = []
        for line in input_file:
            if not line.strip():
                if this_board:
                    boards.append([set(line) for line in this_board] + list(rows_to_cols(this_board)))
                this_board = []
                continue
            this_board.append([int(num) for num in line.split()])
    return balls, boards


def is_board_winner(board):
    return any(len(row_or_col) == 0 for row_or_col in board)


def board_score(board):
    return sum(chain.from_iterable(board)) // 2


def mark_board(board, ball):
    for row_or_col in board:
        row_or_col.discard(ball)


def part_one(balls, boards):
    for ball in balls:
        for board in boards:
            mark_board(board, ball)
            if is_board_winner(board):
                return board_score(board) * ball


def part_two(balls, boards):
    remaining_boards = {i: board for i, board in enumerate(boards)}
    for ball in balls:
        for i, board in list(remaining_boards.items()):
            mark_board(board, ball)
            if is_board_winner(board):
                del remaining_boards[i]
                if len(remaining_boards) == 0:
                    return board_score(board) * ball


print(f"Part One: {part_one(*load_input('input.txt'))}")
print(f"Part Two: {part_two(*load_input('input.txt'))}")

