with open("./day08.input") as file:
	lines = file.readlines()
	lines = [line.strip() for line in lines]

instructions = [(line.split(" ")[0], int(line.split(" ")[1])) for line in lines]

def get_acc_after_repeat():
	acc = 0

	i = 0
	i_visited = []
	while i < len(instructions):
		if i in i_visited:
			break

		i_visited.append(i)
		cmd, amt = instructions[i]
		if cmd == "acc":
			acc += amt
			i += 1
		elif cmd == "nop":
			i += 1
		elif cmd == "jmp":
			i += amt

	return acc

# part1
print(get_acc_after_repeat())

MAX_ATTEMPTS = 10000

def get_acc_with_switching_nop_or_jmp():
	i = 0
	while i < len(instructions):
		attempts = 0

		acc = 0
		j = 0
		while j < len(instructions):
			# infinite instructions ran detected!
			if attempts > MAX_ATTEMPTS:
				break

			cmd, amt = instructions[j]

			if i == j:
				# jmp would go to same instruction
				if cmd == "nop" and amt == j:
					pass
				elif cmd == "jmp":
					cmd = "nop"
				elif cmd == "nop":
					cmd = "jmp"

			if cmd == "acc":
				acc += amt
				j += 1
			elif cmd == "nop":
				j += 1
			elif cmd == "jmp":
				j += amt

			attempts += 1

		# program terminated successfully!
		if attempts < MAX_ATTEMPTS:
			return acc

		i += 1

	return acc

# part2
print(get_acc_with_switching_nop_or_jmp())