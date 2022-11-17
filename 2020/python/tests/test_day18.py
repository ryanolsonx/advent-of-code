from aoc.day18 import *

def test_eval1():
  assert eval1('1 + 2 * 3 + 4 * 5 + 6') == 71
  assert eval1('(4 * 5)') == 20
  assert eval1('2 * 3 + (4 * 5)') == 26
  assert eval1('2 * 3 + (4 * 5) + (2 + 1)') == 29
  assert eval1('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
  assert eval1('1 + (2 + (3 + 4))') == 10
  assert eval1('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
  assert eval1('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

def test_eval2():
  assert eval2('4 * 5 + 6') == 44
  assert eval2('6 + 5 * 4') == 44
  assert eval2('1 + (6 + 5 * 4)') == 45
  assert eval2('1 + (2 * 3) + (4 * (5 + 6))') == 51
  assert eval2('2 * 3 + (4 * 5)') == 46
  assert eval2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
  assert eval2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
  assert eval2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340