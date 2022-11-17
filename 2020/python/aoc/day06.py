def part1(input):
	total = 0
	current_group_letters = ''

	for line in input:
		if line == '':
			total += len(set(current_group_letters))
			current_group_letters = ''
		else:
			current_group_letters += line

	return total

def part2(input):
	total = 0
	i_in_group = 0
	current_group_letters = []

	for line in input:
		if line == '':
			total += len(current_group_letters)
			current_group_letters = []
			i_in_group = 0
		else:
			if i_in_group == 0:
				for letter in line:
					current_group_letters.append(letter)
			else:
				for letter in current_group_letters.copy():
					if not letter in line:
						current_group_letters.remove(letter)
			i_in_group += 1

	return total


if __name__ == '__main__':
	input = [line.strip() for line in open('day06.input', 'r').readlines()]

	p1 = part1(input)
	assert p1 == 6387
	print(p1)

	p2 = part2(input)
	assert p2 == 3039
	print(p2)
