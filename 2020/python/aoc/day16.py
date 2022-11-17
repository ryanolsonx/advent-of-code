# Input:
# 1. rules for ticket fields
#     a. list of fields that exist somewhere on the ticket
#     b. the valid ranges of values for each field
#
#     example: a rule like "class: 1-3 or 5-7" means that one of the fields
#              in every ticket is named class and can be any value in the
#              ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both
#              valid in this field, but 4 is not).
# 2. numbers on your ticket
#     a. The values are the numbers on the ticket in the order they appear
# 3. numbers on other nearby tickets

# the first number is always the same specific field,
# the second number is always a different specific field,
# and so on - you just don't know what each position actually means!

# PART 1: Start by determining which tickets are completely invalid
# ------------
# these are tickets that contain values which aren't valid for any field.
# Ignore your ticket for now.

import math


class Rule:
  def __init__(self, s):
    parts = s.split(': ')

    self.field = parts[0]

    ranges = parts[1].split(' or ')

    self.ranges = [self.parse_range(r) for r in ranges]

  def parse_range(self, rangestr):
    n1, n2 = [int(n) for n in rangestr.split('-')]
    return (n1, n2)

  def is_valid(self, n):
    for range in self.ranges:
      l, u = range
      if u >= n >= l:
        return True

    return False

  def __eq__(self, other):
    return (
      self.field == other.field and
      self.ranges == other.ranges
    )

  def __repr__(self):
    rv = f'Rule(name={self.field}, '

    for r in self.ranges:
      a, b = r

      rv += f'{a}-{b} '
    rv += ')'
    return rv;


class Ticket:
  def __init__(self, nstr):
    self.ns = [int(n) for n in nstr.split(',')]

  def __eq__(self, other):
    return self.ns == other.ns

  def __repr__(self):
    return f'Ticket({self.ns})'


def parse_input(filename):
  rule_block, ticket_block, nearby_tickets_block = (
    open(filename).read().strip().split('\n\n')
  )

  rules = [Rule(rule_def) for rule_def in rule_block.split('\n')]
  ticket = Ticket(ticket_block.split('\n')[1])
  nearby_tickets = [
    Ticket(ticket_def)
    for ticket_def
    in nearby_tickets_block.split('\n')[1:]
  ]

  return rules, ticket, nearby_tickets


def get_error_rate_for_tickets(rules, tickets):
  error_rate = 0

  for ticket in tickets:
    error_rate += get_error_rate_for_ticket(rules, ticket)

  return error_rate


def get_error_rate_for_ticket(rules, ticket):
  error_rate = 0

  for n in ticket.ns:
    valid_for_any = False
    for rule in rules:
      if rule.is_valid(n):
        valid_for_any = True

    if not valid_for_any:
      error_rate += n

  return error_rate


def is_ticket_valid(rules, ticket):
  for n in ticket.ns:
    valid_for_any = False
    for rule in rules:
      if rule.is_valid(n):
        valid_for_any = True

    if not valid_for_any:
      return False

  return True


def get_valid_tickets(rules, tickets):
  return [ticket for ticket in tickets if is_ticket_valid(rules, ticket)]


def get_field_index_for_rule(rule, tickets, used_i):
  fields_count = len(tickets[0].ns)

  i = 0
  while i < fields_count:
    if i in used_i:
      i += 1
      continue

    total_valid = len([
      ticket
      for ticket in tickets
      if rule.is_valid(ticket.ns[i])
    ])

    # print(f'total_valid == len(tickets): {total_valid} == {len(tickets)}')

    if total_valid == len(tickets):
      return i
    i += 1

  print(f'problem rule: {rule}')
  return None


def get_all_possible_field_indexes_for_rule(rule, tickets):
  rv = []

  fields_count = len(tickets[0].ns)
  i = 0
  while i < fields_count:
    i_works = True
    for ticket in tickets:
      n = ticket.ns[i]
      if not rule.is_valid(n):
        i_works = False

    if i_works:
      rv.append(i)

    i += 1

  return rv


def determine_field_order(rules, tickets):
  fields_count = len(tickets[0].ns)
  order = [None] * fields_count
  all_possible = [n for n in range(fields_count)]

  # [(field_name, possible)]
  rule_possibilities = []

  for rule in rules:
    possible = get_all_possible_field_indexes_for_rule(rule, tickets)
    rule_possibilities.append((rule.field, possible))

  # i is ALWAYS field index
  used_i = []

  def by_len(rule_possibility):
    _, possible = rule_possibility
    return len(possible)

  while len(all_possible) > 0:
    poss = []
    for rule_possibility in rule_possibilities:
      field_name, possible = rule_possibility
      possible = [x for x in possible if x not in used_i]

      if len(possible) > 0:
        poss.append((field_name, possible))

    poss = sorted(poss, key=by_len)
    field_name, possible = poss[0]
    i = possible[0]

    used_i.append(i)
    order[i] = field_name
    all_possible.remove(i)

  return order


def get_field_values_starting_with(ticket, order, starting_with):
  rv = []

  i = 0
  while i < len(order):
    n = ticket.ns[i]
    o = order[i]

    if o.startswith(starting_with):
      rv.append(n)

    i += 1

  return rv


def multiply_departure_ticket_values(ticket, order):
  ns = get_field_values_starting_with(ticket, order, 'departure')

  return math.prod(ns)


if __name__ == '__main__':
  rules, ticket, nearby_tickets = parse_input('./aoc/day16.input.txt')

  print(f'part 1: {get_error_rate_for_tickets(rules, nearby_tickets)}')

  tickets = get_valid_tickets(rules, [ticket] + nearby_tickets)
  order = determine_field_order(rules, tickets)
  print(order)

  p2 = multiply_departure_ticket_values(ticket, order)
  print(f'part 2: {p2}')
  assert p2 != 1409959524847


# my_ticket = [int(n) for n in my_ticket.split("\n")[1].split(",")]
# nearby_tickets = [[int(x) for x in n.split(",")] for n in nearby_tickets.split("\n")[1:]]
