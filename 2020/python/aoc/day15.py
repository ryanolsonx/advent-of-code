from collections import defaultdict 

starting_numbers = "9,3,1,0,8,4"
starting_numbers = [int(x) for x in starting_numbers.split(",")]

def get_last_spoken_for(MAX):
  mem = defaultdict()
  for turn in range(1, len(starting_numbers) + 1):
    mem[starting_numbers[turn - 1]] = [turn]

  [last_spoken] = starting_numbers[-1:]

  for turn in range(len(starting_numbers) + 1, MAX + 1):
    m = mem[last_spoken]

    if len(m) == 1:
      a = 0
    else:
      n2, n1 = m[-2:]
      a = n1 - n2

    try:
      # cache last two answers
      last_turn = mem[a][len(mem[a]) - 1]
      mem[a] = [last_turn, turn]
    except KeyError:
      mem[a] = [turn]

    last_spoken = a

  return last_spoken

# print(get_last_spoken_for(2020))
print(get_last_spoken_for(30000000))
