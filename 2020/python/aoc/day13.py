#!/usr/bin/env python3
# fn = "./day13.ex.txt"
fn = "./day13.input.txt"
lines = open(fn).read().strip().split("\n")

start = int(lines[0])

buses = [int(bus) for bus in lines[1].split(",") if bus != "x"]
buses.sort()

nearest = None
waiting_time = None
i = start
while nearest == None:
  for bus in buses:
    if i % bus == 0:
      nearest = bus
      waiting_time = i - start
      break
  i += 1

print("bus: " + str(nearest))
print("waited: " + str(waiting_time) + " mins")

print("part1", nearest * waiting_time)

buses = [bus for bus in lines[1].split(",")]
print(buses)

def naive_approach():
  time = 0
  while True:
    all_work = True
    for i in range(len(buses)):
      if buses[i] != "x" and (time + i) % int(buses[i]) != 0:
        all_work = False

    if all_work:
      print(time)
      break

    time += 1

def mod_inv(n, mod_by):
  n = n % mod_by
  for x in range(1, mod_by):
    if ((n * x) % mod_by == 1):
      return x
  return 1

items = []
full_product = 1
for i in range(len(buses)):
  bus_id = buses[i]
  if bus_id == "x":
    continue
  k = int(bus_id)
  i = i % k
  ai = (k - i) % k
  items.append((ai, k))
  full_product *= k

total = 0
for ai, k in items:
  partial_product = full_product // k
  ni = mod_inv(partial_product, k)
  assert ni * partial_product % k == 1

  term = ni * partial_product * ai
  total += term

print(total % full_product)
