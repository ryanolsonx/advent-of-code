from aoc.day17 import is_active, is_inactive, input_to_active, EXAMPLE_INPUT

def test_is_active():
  assert is_active('#')
  assert not is_active('.')

def test_is_inactive():
  assert is_inactive('.')
  assert not is_inactive('#')

def test_input_to_active():
  assert input_to_active(EXAMPLE_INPUT) == set([
    (2, 2, 0, 0),
    (1, 2, 0, 0),
    (0, 2, 0, 0),
    (2, 1, 0, 0),
    (1, 0, 0, 0),
  ])
