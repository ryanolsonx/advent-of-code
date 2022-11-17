#!/usr/bin/env python3

#fn = "./day11.ex.txt"
fn = "./day11.input.txt"
dat = open(fn).read().strip().split("\n")
dat = [list(line) for line in dat]


FLOOR, OCCUPIED, EMPTY = ".#L"
DIRECTIONS = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]


def get_total_occupied_seats_around(layout, row_idx, col_idx):
  total = 0
  for direction in DIRECTIONS:
    x, y = direction 
    cy = row_idx + y
    cx = col_idx + x
    if in_bounds(layout, cx, cy):
      if layout[cy][cx] == OCCUPIED:
        total += 1
  return total


def get_next_seatp1(layout, row_idx, col_idx, seat):
  if seat == FLOOR:
    return seat

  total_occupied = get_total_occupied_seats_around(layout, row_idx, col_idx)

  if seat == OCCUPIED and total_occupied >= 4:
    return EMPTY
  elif seat == EMPTY and total_occupied == 0:
    return OCCUPIED
  else:
    return seat


def in_bounds(layout, x, y):
  return y >= 0 and y < len(layout) and x >= 0 and x < len(layout[y])


def get_total_occupied_seats_in_sight(layout, row_idx, col_idx):
  total = 0
  for direction in DIRECTIONS:
    x, y = direction 
    cy = row_idx + y
    cx = col_idx + x
    while True:
      if not in_bounds(layout, cx, cy):
        break

      if layout[cy][cx] == OCCUPIED:
        total += 1

      if layout[cy][cx] == OCCUPIED or layout[cy][cx] == EMPTY:
        break

      cy += y
      cx += x
      
  return total


def get_next_seatp2(layout, row_idx, col_idx, seat):
  if seat == FLOOR:
    return seat

  total_occupied = get_total_occupied_seats_in_sight(layout, row_idx, col_idx)

  if seat == OCCUPIED and total_occupied >= 5:
    return EMPTY
  elif seat == EMPTY and total_occupied == 0:
    return OCCUPIED
  else:
    return seat


def run_round(layout, get_next_seat):
  next_layout = []
  for row_idx, row in enumerate(layout):
    next_row = []
    for col_idx, seat in enumerate(row):
      next_row.append(get_next_seat(layout, row_idx, col_idx, seat))
    next_layout.append(next_row)

  return next_layout


def pretty_print(layout):
  str = ""
  for row_idx, row in enumerate(layout):
    for col in layout[row_idx]:
      str += col.strip()
    str += "\n"

  print(str)


def get_total_occupied_in_layout(layout):
  total = 0
  for row in layout:
    for seat in row:
      if seat == OCCUPIED:
        total += 1

  return total


def run(get_next_seat):
  layout = dat[:]
  last_total_occupied = 0
  while True:
    layout = run_round(layout, get_next_seat)
    total = get_total_occupied_in_layout(layout)
    if total == last_total_occupied:
      print(total)
      break
    last_total_occupied = total

# part1
run(get_next_seatp1)

# part2
run(get_next_seatp2)
