#!/usr/bin/env python3
import re


def parse_data(lines):
    passports = []
    passport = {}
    for line in lines:
        if line.strip() == "":
            if len(passport):
                passports.append(passport)
                passport = {}
            continue
        for kv in line.split():
            k, v = kv.split(":")
            passport[k] = v

    if len(passport):
        passports.append(passport)
    return passports


def passport_has_valid_fields(passport):
    return all(k in passport for k in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])


HCL_RE = re.compile(r'^#[\da-f]{6}$')
PID_RE = re.compile(r'^\d{9}$')
HGT_RE = re.compile(r'^(?P<value>\d+)(?P<unit>cm|in)$')


def hgt_valid(hgt):
    match = HGT_RE.match(hgt)
    if not match:
        return False
    if match.group("unit") == "cm":
        return 150 <= int(match.group("value")) <= 193
    if match.group("unit") == "in":
        return 59 <= int(match.group("value")) <= 76



def passport_is_valid(passport):
    return 1920 <= int(passport["byr"]) <= 2002 \
           and 2010 <= int(passport["iyr"]) <= 2020 \
           and 2020 <= int(passport["eyr"]) <= 2030 \
           and hgt_valid(passport["hgt"]) \
           and HCL_RE.match(passport["hcl"]) \
           and passport["ecl"] in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth") \
           and PID_RE.match(passport["pid"])


with open("input.txt") as puzzle_input:
    PASSPORTS = parse_data(puzzle_input.readlines())

PASSPORTS_WITHOUT_MISSING_DATA = list(filter(passport_has_valid_fields, PASSPORTS))
print(f"Part One: {len(PASSPORTS_WITHOUT_MISSING_DATA)}")
print(f"Part Two: {sum(1 for passport in PASSPORTS_WITHOUT_MISSING_DATA if passport_is_valid(passport))}")
