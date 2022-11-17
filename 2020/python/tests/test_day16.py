from aoc.day16 import Rule, Ticket, get_error_rate_for_tickets, \
  get_error_rate_for_ticket, parse_input, is_ticket_valid, \
  get_valid_tickets, determine_field_order, get_field_index_for_rule, \
  get_field_values_starting_with, multiply_departure_ticket_values, \
  get_all_possible_field_indexes_for_rule


def test_parse_input():
  rules, ticket, nearby_tickets = parse_input('./aoc/day16.ex.txt')
  assert rules == [
    Rule('class: 1-3 or 5-7'),
    Rule('row: 6-11 or 33-44'),
    Rule('seat: 13-40 or 45-50'),
  ]

  assert ticket == Ticket('7,1,14')

  assert nearby_tickets == [
    Ticket('7,3,47'),
    Ticket('40,4,50'),
    Ticket('55,2,20'),
    Ticket('38,6,12'),
  ]


def test_rule_init():
  rule = Rule('class: 1-3 or 5-7')

  assert rule.field == 'class'
  assert rule.ranges == [(1, 3), (5, 7)]

  rule = Rule('arrival platform: 29-826 or 846-958')

  assert rule.field == 'arrival platform'
  assert rule.ranges == [(29, 826), (846, 958)]


def test_rule_equality():
  assert Rule('class: 1-3 or 5-7') == Rule('class: 1-3 or 5-7')


def test_rule_is_valid():
  rule = Rule('class: 1-3 or 5-7')
  check_range(rule, 1, 3, 5, 7)

  rule = Rule('arrival platform: 29-826 or 846-958')
  check_range(rule, 29, 826, 846, 958)

  rule = Rule('seat: 13-40 or 45-50')
  assert rule.is_valid(50)


def check_range(rule, start1, end1, start2, end2):
  for n in range(start1 - 1000, start1 - 1):
    assert not rule.is_valid(n)

  for n in range(start1, end1):
    assert rule.is_valid(n)

  for n in range(end1 + 1, start2 - 1):
    assert not rule.is_valid(n)

  for n in range(start2, end2):
    assert rule.is_valid(n)

  for n in range(end2 + 1, end2 + 1000):
    assert not rule.is_valid(n)


def test_ticket_init():
  ticket = Ticket('149,73,71,107,113,151,223,67,163')
  assert ticket.ns == [ 149, 73, 71, 107, 113, 151, 223, 67, 163 ]


def test_ticket_equality():
  assert Ticket('7,1,14') == Ticket('7,1,14')


def test_get_error_rate_for_ticket():
  rules = [
    Rule('class: 1-3 or 5-7'),
    Rule('row: 6-11 or 33-44'),
    Rule('seat: 13-40 or 45-50'),
  ]

  ticket = Ticket('7,3,47')
  assert get_error_rate_for_ticket(rules, ticket) == 0

  ticket = Ticket('40,4,50')
  assert get_error_rate_for_ticket(rules, ticket) == 4

  ticket = Ticket('55,2,20')
  assert get_error_rate_for_ticket(rules, ticket) == 55

  ticket = Ticket('38,6,12')
  assert get_error_rate_for_ticket(rules, ticket) == 12


def test_get_error_rate_for_tickets():
  rules = [
    Rule('class: 1-3 or 5-7'),
    Rule('row: 6-11 or 33-44'),
    Rule('seat: 13-40 or 45-50'),
  ]

  nearby_tickets = [
    Ticket('7,3,47'),
    Ticket('40,4,50'),
    Ticket('55,2,20'),
    Ticket('38,6,12'),
  ]

  assert get_error_rate_for_tickets(rules, nearby_tickets) == 71


def test_is_ticket_valid():
  rules = [
    Rule('class: 1-3 or 5-7'),
    Rule('row: 6-11 or 33-44'),
    Rule('seat: 13-40 or 45-50'),
  ]

  ticket = Ticket('7,3,47')
  assert is_ticket_valid(rules, ticket)

  ticket = Ticket('40,4,50')
  assert not is_ticket_valid(rules, ticket)

  ticket = Ticket('55,2,20')
  assert not is_ticket_valid(rules, ticket)

  ticket = Ticket('38,6,12')
  assert not is_ticket_valid(rules, ticket)


def test_get_valid_tickets():
  rules = [
    Rule('class: 1-3 or 5-7'),
    Rule('row: 6-11 or 33-44'),
    Rule('seat: 13-40 or 45-50'),
  ]

  assert get_valid_tickets(rules, [
    Ticket('7,3,47'),
    Ticket('40,4,50'),
    Ticket('55,2,20'),
    Ticket('38,6,12'),
  ]) == [Ticket('7,3,47')]


def test_get_field_index_for_rule():
  rule = Rule('class: 0-1 or 4-19')
  tickets = [
    Ticket('11,12,13'),
    Ticket('3,9,18'),
    Ticket('15,1,5'),
    Ticket('5,14,9'),
  ]

  assert get_field_index_for_rule(rule, tickets, []) == 1

  rule = Rule('bar: 0-4 or 5-10')
  tickets = [
    Ticket('1, 10, 20, 30'),
    Ticket('2, 9, 20, 30'),
    Ticket('1, 6, 20, 30'),
    Ticket('4, 7, 20, 30'),
  ]

  assert get_field_index_for_rule(rule, tickets, [0]) == 1

def test_get_all_possible_field_indexes_for_rule():
  rules = [
    Rule('train: 0-2 or 4-19'),
    Rule('car: 0-5 or 8-19'),
    Rule('date: 0-13 or 16-19'),
  ]

  tickets = [
    Ticket('3,9,18'),
    Ticket('2,10,16'),
    Ticket('5,13,15'),
  ]

  v = get_all_possible_field_indexes_for_rule(rules[0], tickets)
  assert v == [1, 2]


def test_determine_field_order():
  rules, ticket, nearby_tickets = parse_input('./aoc/day16.ex2.txt')
  tickets = get_valid_tickets(rules, nearby_tickets)

  v = determine_field_order(rules, tickets)
  assert v == ['row', 'class', 'seat']


def test_get_field_values_starting_with():
  order = [
    'departure location',
    'arrival location',
    'arrival track',
    'departure station',
    'class',
    'duration',
    'departure track',
    'departure platform',
  ]

  ticket = Ticket('149,73,71,107,113,151,223,67')

  v = get_field_values_starting_with(ticket, order, 'departure')
  assert v == [149, 107, 223, 67]


def test_multiply_departure_ticket_values():
  order = [
    'departure location',
    'arrival location',
    'arrival track',
    'departure station',
    'class',
    'duration',
    'departure track',
    'departure platform',
  ]

  ticket = Ticket('149,73,71,107,113,151,223,67')

  v = multiply_departure_ticket_values(ticket, order)
  assert v == (149 * 107 * 223 * 67)
