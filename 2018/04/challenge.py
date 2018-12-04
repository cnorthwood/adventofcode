#!/usr/bin/env pypy3

from collections import Counter, defaultdict
from datetime import datetime
import re

INPUT_RE = re.compile(r'\[(?P<y>\d\d\d\d)-(?P<mo>\d\d)-(?P<d>\d\d) (?P<h>\d\d):(?P<mi>\d\d)\] (?P<event>.+)')
SHIFT_RE = re.compile(r'Guard #(?P<guard>\d+) begins shift')


def load_events(filename):
    events = set()
    with open(filename) as input_file:
        for line in input_file:
            match = INPUT_RE.match(line)
            events.add(
                (datetime(int(match.group('y')),
                          int(match.group('mo')),
                          int(match.group('d')),
                          int(match.group('h')),
                          int(match.group('mi')),
                         ),
                 match.group('event'),
                )
            )
    return sorted(events, key=lambda item: item[0])


def group_shifts(events):
    shift_events = None
    guard = None
    for dt, event in events:
        shift_match = SHIFT_RE.match(event)
        if shift_match is not None:
            if shift_events is not None:
                yield guard, shift_events
            guard = shift_match.group('guard')
            shift_events = []
        else:
            shift_events.append((dt, event))
    yield guard, shift_events


def build_sleep_ranges(shifts):
    sleep_minutes = defaultdict(Counter)
    for guard, events in shifts:
        for sleep, wake in zip(events[::2], events[1::2]):
            for m in range(sleep[0].minute, wake[0].minute):
                sleep_minutes[guard][m] += 1
    return sleep_minutes


def part_one(sleep_minutes):
    sleepiest_guard = max(sleep_minutes.keys(), key=lambda k: sum(sleep_minutes[k].values()))
    sleepiest_minute = max(sleep_minutes[sleepiest_guard].keys(), key=lambda k: sleep_minutes[sleepiest_guard][k])
    return int(sleepiest_guard) * sleepiest_minute


# test_sleep_minutes = build_sleep_ranges(group_shifts(load_events('test.txt')))
SLEEP_MINUTES = build_sleep_ranges(group_shifts(load_events('input.txt')))

# assert(part_one(test_sleep_minutes) == 240)
print("Part One: {}".format(part_one(SLEEP_MINUTES)))


def part_two(sleep_minutes):
    most_slept_guard_minute = list(map(lambda item: (item[0], max(item[1].items(), key=lambda k: k[1])), sleep_minutes.items()))
    most_slept_guard, most_slept_minute = max(most_slept_guard_minute, key=lambda k: k[1][1])
    return int(most_slept_guard) * most_slept_minute[0]


# assert(part_two(test_sleep_minutes) == 4455)
print("Part Two: {}".format(part_two(SLEEP_MINUTES)))
