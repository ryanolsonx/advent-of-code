from collections import defaultdict
import math

# fn = "./day14.ex.txt"
fn = "./day14.input.txt"
lines = open(fn).read().strip().split("\n")


def num_to_binary_string(value):
  """ convert to binary and make len 36 (padded with zeroes) as list """
  return list(bin(int(value))[2:].rjust(36, '0'))


def binary_string_to_num(bvalue):
  """ convert from binary string (as list of chars)to int """
  return int("".join(bvalue), 2)


def apply_mask(mask, value):
  # convert to binary and make len 36 (padded with zeroes)
  bvalue = num_to_binary_string(value)
  ret = bvalue
  for i in range(len(mask)):
    ret[i] = bvalue[i] if mask[i] == "X" else mask[i]

  return binary_string_to_num(ret)


def add_all_mem_values(mem):
  total = 0
  for i in mem:
    total += mem[i]

  return total


# part 1
mem = defaultdict(int)
for instr in lines:
  var, val = instr.split(" = ")
  if var.startswith("mask"):
    mask = val
  if var.startswith("mem"):
    i = int(var[4:-1])
    mem[i] = apply_mask(mask, val)

print(add_all_mem_values(mem))


# part 2
def apply_mask2(mask, i):
  bvalue = num_to_binary_string(i)
  masked = bvalue
  for i in range(len(mask)):
    m = mask[i]
    if m == "1":
      masked[i] = "1"
    elif m == "X":
      masked[i] = "X"
    else:
      masked[i] = bvalue[i]

  return masked

def get_mask_memory_locations(mask, i):
  masked = apply_mask2(mask, i)
  total_xs = len([x for x in masked if x == "X"])
  combinations = int(math.pow(2, total_xs))

  rets = []
  for i in range(combinations):
    ibinary = list(bin(i)[2:].rjust(total_xs, '0'))

    ret = masked.copy()
    xi = 0
    for j in range(len(masked)):
      if masked[j] == "X":
        ret[j] = ibinary[xi]
        xi += 1
      else:
        ret[j] = masked[j]
    rets.append(binary_string_to_num(ret))

  return rets

mem = defaultdict(int)
for instr in lines:
  var, val = instr.split(" = ")
  if var.startswith("mask"):
    mask = val
  if var.startswith("mem"):
    i = int(var[4:-1])
    v = int(val)
    for loc in get_mask_memory_locations(mask, i):
      mem[loc] = v

print(add_all_mem_values(mem))
