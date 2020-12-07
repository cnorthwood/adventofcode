#!/usr/bin/env python3

def seat_code_to_bitfield(seat_code):
    seat_bitfield = 0
    row_describers = seat_code[:7]
    col_describers = seat_code[7:11]
    for i, row_describer in enumerate(row_describers):
        if row_describer == "F":
            this_bit = 1 << i
            seat_bitfield |= this_bit
    for i, col_describer in enumerate(col_describers):
        if col_describer == "L":
            this_bit = 1 << (i + 7)
            seat_bitfield |= this_bit
    return seat_bitfield


def seat_id(seat_code):
    row_range = (0, 127)
    col_range = (0, 7)
    for i in range(7):
        row_describer = bool(seat_code & (1 << i))
        d = (row_range[1] - row_range[0]) // 2
        if row_describer:
            row_range = row_range[0], row_range[0] + d
        else:
            row_range = row_range[1] - d, row_range[1]
    for i in range(7, 10):
        col_describer = bool(seat_code & (1 << i))
        d = (col_range[1] - col_range[0]) // 2
        if col_describer:
            col_range = col_range[0], col_range[0] + d
        else:
            col_range = col_range[1] - d, col_range[1]

    return row_range[0] * 8 + col_range[0]


def is_my_seat(seat_code, all_seat_codes, all_seat_ids):
    this_seat_id = seat_id(seat_code)
    if seat_code in all_seat_codes:
        return False
    return this_seat_id - 1 in all_seat_ids and this_seat_id + 1 in all_seat_ids


with open("input.txt") as input_file:
    SEAT_CODES = {seat_code_to_bitfield(line) for line in input_file.readlines()}

ALL_SEAT_IDS = {seat_id(seat_code) for seat_code in SEAT_CODES}
print(f"Part One: {max(ALL_SEAT_IDS)}")
for seat_code in range(2**11):
    if is_my_seat(seat_code, SEAT_CODES, ALL_SEAT_IDS):
        print(f"Part Two: {seat_id(seat_code)}")
        break
