input = [line.strip() for line in open('day03.input', 'r').readlines()]

def count_trees_in_path(map, X, Y):
	trees = 0
	y = Y
	x = X
	max = len(map[0])
	while y < len(map):
		if map[y][x] == '#':
			trees += 1
		y += Y
		x = (x + X) % max

	return trees

def part1():
	return count_trees_in_path(input, 3, 1)

print(part1())

def part2():
	total_trees_hit = 1
	for slope in ([1, 1], [3, 1], [5, 1], [7, 1], [1, 2]):
		total_trees_hit *= count_trees_in_path(input, slope[0], slope[1])
	return total_trees_hit

print(part2())
