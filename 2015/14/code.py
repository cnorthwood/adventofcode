import re

class Reindeer(object):

    @classmethod
    def from_line(cls, line):
        return cls(*map(int, re.match(r'\w+ can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.', line).groups()))

    def __init__(self, speed, travel_time, rest_time):
        self._state = 'flying'
        self._time_in_state = 0
        self.distance = 0
        self._speed = speed
        self._travel_time = travel_time
        self._rest_time = rest_time
        self.points = 0

    def tick(self):
        if self._needs_to_rest():
            self._state = 'resting'
            self._time_in_state = 0

        elif self._ready_to_fly():
            self._state = 'flying'
            self._time_in_state = 0

        if self._in_flight():
            self.distance += self._speed

        self._time_in_state += 1

    def _needs_to_rest(self):
        return self._state == 'flying' and self._time_in_state == self._travel_time

    def _in_flight(self):
        return self._state == 'flying' and self._time_in_state < self._travel_time

    def _ready_to_fly(self):
        return self._state == 'resting' and self._time_in_state == self._rest_time

INPUT = """Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds.
Cupid can fly 22 km/s for 2 seconds, but then must rest for 41 seconds.
Rudolph can fly 11 km/s for 5 seconds, but then must rest for 48 seconds.
Donner can fly 28 km/s for 5 seconds, but then must rest for 134 seconds.
Dasher can fly 4 km/s for 16 seconds, but then must rest for 55 seconds.
Blitzen can fly 14 km/s for 3 seconds, but then must rest for 38 seconds.
Prancer can fly 3 km/s for 21 seconds, but then must rest for 40 seconds.
Comet can fly 18 km/s for 6 seconds, but then must rest for 103 seconds.
Vixen can fly 18 km/s for 5 seconds, but then must rest for 84 seconds."""

TIME = 2503

REINDEERS = map(Reindeer.from_line, INPUT.splitlines())

def leading_distance():
    return max(map(lambda r: r.distance, REINDEERS))

for _ in xrange(TIME):
    for reindeer in REINDEERS: reindeer.tick()
    for reindeer in filter(lambda r: r.distance == leading_distance(), REINDEERS): reindeer.points += 1

print "Part One", leading_distance()
print "Part Two", max(map(lambda r: r.points, REINDEERS))
