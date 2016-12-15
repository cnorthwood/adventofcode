from collections import defaultdict
import re
from itertools import chain

import operator

VALUE_RE = re.compile(r'value (?P<value>\d+) goes to bot (?P<bot>\d+)')
ACTION_RE = re.compile(r'bot (?P<bot>\d+) gives low to (?P<low_target_type>(bot|output)) (?P<low_target_id>\d+) and high to (?P<high_target_type>(bot|output)) (?P<high_target_id>\d+)')


class Bot(object):

    def __init__(self):
        self._chips = set()
        self._low_target_type = None
        self._low_target_id = None
        self._high_target_type = None
        self._high_target_id = None

    def set_action(self, low_target_type, low_target_id, high_target_type, high_target_id, **kwargs):
        self._low_target_type = low_target_type
        self._low_target_id = low_target_id
        self._high_target_type = high_target_type
        self._high_target_id = high_target_id

    def take(self, chip):
        self._chips.add(int(chip))

    def act(self):
        if len(self._chips) == 2:
            low, high = sorted(self._chips)
            if self._low_target_type == 'bot':
                BOTS[self._low_target_id].take(low)
            elif self._low_target_type == 'output':
                OUTPUTS[self._low_target_id].add(low)
            if self._high_target_type == 'bot':
                BOTS[self._high_target_id].take(high)
            elif self._high_target_type == 'output':
                OUTPUTS[self._high_target_id].add(high)
            self._chips = set()

    def check(self):
        return 61 in self._chips and 17 in self._chips


BOTS = defaultdict(Bot)
OUTPUTS = defaultdict(set)

with open('input.txt') as input:
    for line in input:
        value_match = VALUE_RE.match(line)
        action_match = ACTION_RE.match(line)
        if value_match:
            BOTS[value_match.groupdict().get('bot')].take(value_match.groupdict().get('value'))
        elif action_match:
            BOTS[action_match.groupdict().get('bot')].set_action(**action_match.groupdict())
        else:
            print "Unrecognised", line
            break


def get_part_one_comparator():
    while True:
        for bot_id, bot in BOTS.iteritems():
            bot.act()
        for bot_id, bot in BOTS.iteritems():
            if bot.check():
                return bot_id


def get_part_two_sum():
    while not (len(OUTPUTS['0']) == 1 and len(OUTPUTS['1']) == 1 and len(OUTPUTS['2']) == 1):
        for bot in BOTS.values():
            bot.act()
    return reduce(operator.mul, chain(OUTPUTS['0'], OUTPUTS['1'], OUTPUTS['2']))


print "Part One:", get_part_one_comparator()
print "Part Two:", get_part_two_sum()
