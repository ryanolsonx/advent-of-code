import math

ROWS = 127
COLS = 7

def get_seat(instruction, c = 0, C = COLS, r = 0, R = ROWS):
	if (len(instruction) > 0):
		i = instruction[0]
		R = math.floor(((R - r) / 2) + r) if i == "F" else R
		r = math.ceil(((R - r) / 2) + r) if i == "B" else r
		C = math.floor(((C - c) / 2) + c) if i == "L" else C
		c = math.ceil(((C - c) / 2) + c) if i == "R" else c

		return get_seat(instruction[1:], c, C, r, R)
	else:
		return (r * 8) + c

def part1(instructions):
	max_seat_id = 0
	
	for instruction in instructions:
		seat_id = get_seat(instruction)
		if seat_id > max_seat_id:
			max_seat_id = seat_id

	return max_seat_id

def part2(instructions):
	seat_ids = []
	for instruction in instructions:
		seat_ids.append(get_seat(instruction))

	seat_ids = sorted(seat_ids)

	i = 1
	while i < len(seat_ids):
		prev_seat_id = seat_ids[i - 1]
		seat_id = seat_ids[i]
		if (prev_seat_id + 1) != seat_id:
			return seat_id - 1
		i += 1

if __name__ == '__main__':
	input = [line.strip() for line in open('day05.input', 'r').readlines()]

	p1 = part1(input)
	assert p1 == 848
	print(p1)

	p2 = part2(input)
	assert p2 == 682
	print(p2)
