import re

def create_passports(lines):
	passports = []
	passport_lines = []
	for line in lines.split("\n"):
		if line == '':
			passports.append(create_passport(passport_lines))
			passport_lines = []
		else:
			passport_lines.append(line.strip())

	return passports

def create_passport(lines):
	passport = {}
	for line in lines:
		if line == "":
			continue

		kvs = [v.split(":") for v in line.split(" ")]

		for [key, val] in kvs:
			passport[key] = val

	return passport

def has_all_required_fields(passport):
	keys = passport.keys()

	if len(keys) == 8:
		return True
	elif len(keys) == 7:
		return "cid" not in keys
	
	return False

def total_valid_passports(total, passport):
	if has_all_required_fields(passport):
		return total + 1
	return total

def part1(passports):
	total_valid = 0
	for passport in passports:
		if has_all_required_fields(passport):
			total_valid += 1

	return total_valid

def regex(expr):
	def is_valid(v):
		return re.match(expr, v)
	return is_valid

def in_range(min, max):
	def is_valid(v):
		return int(v) >= min and int(v) <= max
	return is_valid

def is_valid_height(height):
	if not (height.endswith('cm') or height.endswith('in')) or len(height) == 2:
		return False

	n = int(height[:-2])

	if height.endswith('cm'):
		return in_range(150, 193)(n)

	# inches
	return in_range(59, 76)(n)

def noop(v):
	return True

validators = {
	'byr': in_range(1920, 2002),
	'iyr': in_range(2010, 2020),
	'eyr': in_range(2020, 2030),
	'hgt': is_valid_height,
	'hcl': regex('^#[0-9a-f]{6}$'),
	'ecl': regex('^amb|blu|brn|gry|grn|hzl|oth$'),
	'pid': regex('^[0-9]{9}$'),
	'cid': noop,
}

def all_fields_valid(passport):
	for k in passport.keys():
		v = passport[k]
		is_valid = validators[k]

		if not is_valid(v):
			return False

	return True

def part2(passports):
	total_valid = 0
	for passport in passports:
		if has_all_required_fields(passport) and all_fields_valid(passport):
			total_valid += 1

	return total_valid

if __name__ == '__main__':
	input = open('day04.input', 'r').read()
	passports = create_passports(input)

	p1 = part1(passports)
	assert p1 == 245
	print(p1)

	p2 = part2(passports)
	assert p2 == 133
	print(p2)
