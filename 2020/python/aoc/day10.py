#!/usr/bin/env python3

f = "day10.input.txt"
# f = "day10.ex.txt"
ns = open(f).read().strip().split("\n")
ns = [int(x) for x in ns]
ns.sort()

ns.insert(0, 0)
ns.append(max(ns) + 3)

def part1():
  count1 = 0
  count3 = 0

  for i in range(len(ns) - 1):
    diff = ns[i + 1] - ns[i]

    if diff == 1:
      count1 += 1

    if diff == 3:
      count3 += 1

  return count1 * count3

checked = {}

def get_num_ways(pos):
  # last
  if pos == len(ns) - 1:
    return 1

  if pos in checked:
    return checked[pos]

  total = 0
  for i in range(pos + 1, len(ns)):
    if ns[i] - ns[pos] <= 3:
      total += get_num_ways(i)

  checked[pos] = total
  return total

def part2():
  return get_num_ways(0)

print(part1())
print(part2())
