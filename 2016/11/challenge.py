import itertools

INITIAL_FLOORS = (
    frozenset([('polonium', 'generator'), ('thulium', 'generator'), ('thulium', 'microchip'), ('promethium', 'generator'),
               ('ruthenium', 'generator'), ('ruthenium', 'microchip'), ('cobalt', 'generator'), ('cobalt', 'microchip'),
               ('elerium', 'generator'), ('elerium', 'microchip'), ('dilithium', 'generator'), ('dilithium', 'microchip')]),
    frozenset([('polonium', 'microchip'), ('promethium', 'microchip')]),
    frozenset(),
    frozenset()
)


def stable((current_floor, floors)):
    for floor in floors:
        microchips = {isotope for isotope, item_type in floor if item_type == 'microchip'}
        generators = {isotope for isotope, item_type in floor if item_type == 'generator'}
        for microchip in microchips:
            if microchip not in generators and len(generators) > 0:
                return False
    else:
        return True


assert stable((1, INITIAL_FLOORS))
assert not stable((1, (frozenset([('polonium', 'generator'), ('thorium', 'microchip')]), frozenset())))


def completed((current_floor, floors)):
    return current_floor == 3 and len(floors[0]) == 0 and len(floors[1]) == 0 and len(floors[2]) == 0


def generate_options((current_floor, floors)):
    for new_items in itertools.product(floors[current_floor], floors[current_floor]):
        new_items = frozenset(new_items)

        if current_floor > 0:
            yield (
                current_floor - 1,
                floors[:current_floor-1] + (frozenset(floors[current_floor-1] | new_items), frozenset(floors[current_floor] - new_items)) + floors[current_floor+1:]
            )

        if current_floor < 3:
            yield (
                current_floor + 1,
                floors[:current_floor] + (frozenset(floors[current_floor] - new_items), frozenset(floors[current_floor+1] | new_items)) + floors[current_floor+2:]
            )


i = 0
options = {(0, INITIAL_FLOORS)}
while not any(completed(option) for option in options):
    i += 1
    print "Iteration {}: {} to check".format(i, len(options))
    next_options = set()
    for option in options:
        next_options |= frozenset(filter(stable, generate_options(option)))
    options = next_options
    if len(options) == 0:
        break

print "Part One:", i
