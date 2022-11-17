def get_lines(input):
  return [x.strip() for x in input.split("\n") if x.strip() != '']


PUZZLE_INPUT = get_lines(
  """

  ...#..#.
  #..#...#
  .....###
  ##....##
  ......##
  ........
  .#......
  ##...#..

  """
)

EXAMPLE_INPUT = get_lines(
  """

  .#.
  ..#
  ###

  """
)

TOTAL_CYCLES = 6


def is_active(cube):
  return cube == '#'


def is_inactive(cube):
  return cube == '.'


def input_to_active(input):
  res = set()
  for y, line in enumerate(input):
    for x, cube in enumerate(line):
      if is_active(cube):
        res.add((x, y, 0, 0))

  return res


if __name__ == '__main__':
  active = input_to_active(PUZZLE_INPUT)

  for _ in range(6):
    to_check = set()
    next_active = set()

    for x, y, z, w in active:
      active_count = 0
      for cx in range(-1, 2):
        for cy in range(-1, 2):
          for cz in range(-1, 2):
            for cw in range(-1, 2):
              cube = (x+cx, y+cy, z+cz, w+cw)
              if cube in active:
                active_count += 1
              else:
                to_check.add(cube)

      if 2 < active_count < 5:
        next_active.add((x, y, z, w))

    # Check neighbors to see if they should turn active
    for x, y, z, w in to_check:
      active_count = 0
      for cx in range(-1, 2):
        for cy in range(-1, 2):
          for cz in range(-1, 2):
            for cw in range(-1, 2):
              if (x+cx, y+cy, z+cz, w+cw) in active:
                active_count += 1

      if active_count == 3:
        next_active.add((x, y, z, w))

    active = next_active

  print(len(active))
