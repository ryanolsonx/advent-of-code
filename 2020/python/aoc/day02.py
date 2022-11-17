input = [line.strip() for line in open('day02.input', 'r').readlines()]

def part1():
	valid = 0
	for x in input:
		[first, password] = x.split(': ')
		[minmax, letter] = first.split(' ');
		[min, max] = minmax.split('-');

		letters_found = len([l for l in password if l == letter])

		if letters_found >= int(min) and letters_found <= int(max):
			valid += 1

	return valid

print(part1())

def part2():
	valid = 0
	for x in input:
		[first, password] = x.split(': ')
		[minmax, letter] = first.split(' ');
		[p1, p2] = minmax.split('-');
		p1 = int(p1)
		p2 = int(p2)

		has_p1 = password[p1 - 1] == letter
		has_p2 = password[p2 - 1] == letter

		if (has_p1 or has_p2) and not (has_p1 and has_p2):
			valid += 1

	return valid

print(part2())
