with open("./day09.input") as file:
	data = [int(line.strip()) for line in file.readlines()]


def get_first_not_matching(preamble_size):
	i = preamble_size
	while i < len(data):
		n = data[i]
		is_match = False
		ds = data[i - preamble_size:i]
		for j in ds:
			for k in ds:
				if j == k:
					continue

				if j + k == n:
					is_match = True
					break
			if is_match:
				break

		if not is_match:
			return n
		i += 1


p1 = get_first_not_matching(25)
print(p1)

def get_min_max(ns):
	min = ns[0]
	max = ns[0]
	for n in ns:
		if n < min:
			min = n
		if n > max:
			max = n
	return (min, max)

def get_contiguous_ns_that_add_to(value):
	i = 0
	while i < len(data):
		n1 = data[i]
		acc = n1
		group = [n1]

		j = i + 1
		while j < len(data):
			n2 = data[j]

			if acc + n2 > value:
				# start over
				break

			group.append(n2)

			if acc + n2 == value:
				min, max = get_min_max(group)
				return min + max
			else:
				acc += n2
			j += 1
		i += 1

p2 = get_contiguous_ns_that_add_to(p1)
print(p2)