#!/usr/bin/env python3

import math


# fn = "./day12.ex.txt"
fn = "./day12.input.txt"
instructions = [(line[0], int(line[1:])) for line in open(fn).read().strip().split("\n")]


# directions
NORTH, EAST, SOUTH, WEST = "NESW"

# actions
ROTATE_LEFT, ROTATE_RIGHT, GO_FORWARD = "LRF"


def go_in_direction(direction, x, y, amt):
  if direction == NORTH:
    return x, y + amt
  elif direction == SOUTH:
    return x, y - amt
  elif direction == EAST:
    return x + amt, y
  elif direction == WEST:
    return x - amt, y


def rotate(facing, by):
  seq = [NORTH, EAST, SOUTH, WEST]
  curr_index = seq.index(facing)

  times = by / 90

  next_index = (curr_index + times) % 4

  return seq[next_index]

facing = EAST
x, y = 0, 0
for instruction in instructions:
  action, amt = instruction
  if action in [NORTH, EAST, SOUTH, WEST]:
  	x, y = go_in_direction(action, x, y, amt)
  elif action == GO_FORWARD:
    x, y = go_in_direction(facing, x, y, amt)
  elif action in [ROTATE_RIGHT, ROTATE_LEFT]:
    facing = rotate(facing, amt if action == ROTATE_RIGHT else amt * -1)

print("part1", int(math.fabs(x) + math.fabs(y)))


def move_waypoint(direction, waypoint, amt):
  x, y = waypoint
  return go_in_direction(direction, x, y, amt)


def move_towards_waypoint(ship, waypoint, amt):
  ship_x, ship_y = ship
  waypoint_x, waypoint_y = waypoint

  for i in range(amt):
    ship_x += waypoint_x
    ship_y += waypoint_y

  return ship_x, ship_y


def rotate_waypoint(action, amt, waypoint):
  times = amt / 90

  x, y = waypoint
  for i in range(times):
    if action == ROTATE_RIGHT:
      x1 = y
      y1 = -1 * x
    else:
      # ROTATE_LEFT
      x1 = -1 * y
      y1 = x
    x, y = x1, y1

  return x, y


waypoint = 10, 1
ship = 0, 0
for instruction in instructions:
  action, amt = instruction
  if action in [NORTH, EAST, SOUTH, WEST]:
    waypoint = move_waypoint(action, waypoint, amt)
  elif action == GO_FORWARD:
    ship = move_towards_waypoint(ship, waypoint, amt)
  elif action in [ROTATE_RIGHT, ROTATE_LEFT]:
    waypoint = rotate_waypoint(action, amt, waypoint)

x, y = ship
print("part2", int(math.fabs(x) + math.fabs(y)))