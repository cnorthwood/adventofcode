#!/usr/bin/env python3

from collections import defaultdict
from queue import Queue, Empty
from threading import Thread


class Execution(Thread):
    def __init__(self, pid, tx_queue, rx_queue, instructions):
        super().__init__()
        self._registers = defaultdict(int)
        self._registers['p'] = pid
        self.send_count = 0
        self._tx_queue = tx_queue
        self._rx_queue = rx_queue
        self._instructions = instructions

    def _deref(self, x):
        try:
            return int(x)
        except:
            return self._registers[x]

    def _snd(self, x):
        self._tx_queue.put(self._deref(x))
        return 1, 1

    def _set(self, x, y):
        self._registers[x] = self._deref(y)
        return 1, 0

    def _add(self, x, y):
        self._registers[x] += self._deref(y)
        return 1, 0

    def _mul(self, x, y):
        self._registers[x] *= self._deref(y)
        return 1, 0

    def _mod(self, x, y):
        self._registers[x] %= self._deref(y)
        return 1, 0

    def _rcv(self, x):
        self._registers[x] = self._rx_queue.get(timeout=5)
        return 1, 0

    def _jgz(self, x, y):
        if self._deref(x) > 0:
            return self._deref(y), 0
        else:
            return 1, 0

    def run(self):
        ops = {
            'snd': self._snd,
            'set': self._set,
            'add': self._add,
            'mul': self._mul,
            'mod': self._mod,
            'rcv': self._rcv,
            'jgz': self._jgz,
        }

        asm = []
        for instruction in self._instructions.strip().splitlines():
            parts = instruction.split()
            asm.append((parts[0], parts[1:]))

        pc = 0
        while 0 <= pc < len(asm):
            op, args = asm[pc]
            try:
                jump, sends = ops[op](*args)
            except Empty:
                break
            pc += jump
            self.send_count += sends


with open('input.txt') as input_file:
    INPUT = input_file.read().strip()

queue_01 = Queue()
queue_10 = Queue()

p0 = Execution(0, queue_01, queue_10, INPUT)
p0.start()
p1 = Execution(1, queue_10, queue_01, INPUT)
p1.start()

p0.join()
p1.join()

print("Part Two:", p1.send_count)
