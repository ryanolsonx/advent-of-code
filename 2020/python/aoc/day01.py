def part1(ns):
  for i in ns:
    for j in ns:
      if i == j:
        continue;

      if i + j == 2020:
        return i * j


def part2(ns):
  for i in ns:
    for j in ns:
      for k in ns:
        if i == j or j == k:
          continue;

        if i + j + k == 2020:
          return i * j * k


if __name__ == '__main__':
  ns = [int(line.strip()) for line in open('./aoc/day01.input', 'r').readlines()]
  print(part1(ns))
  print(part2(ns))
