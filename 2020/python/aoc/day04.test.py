from day04 import create_passport, create_passports, has_all_required_fields, in_range, is_valid_height, regex, validators

def test_create_passport():
	lines = ["ecl:gry pid:860033327 eyr:2020 hcl:#fffffd", "byr:1937 iyr:2017 cid:147 hgt:183cm"]
	assert create_passport(lines) == {
		'ecl': 'gry',
		'pid': '860033327',
		'eyr': 2020,
		'hcl': '#fffffd',
		'byr': 1937,
		'iyr': 2017,
		'cid': 147,
		'hgt': '183cm'
	}

def test_create_passports():
	lines = "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\nbyr:1937 iyr:2017 cid:147 hgt:183cm\n\nhcl:#ae17e1 iyr:2013\neyr:2024\n ecl:brn pid:760753108 byr:1931\n hgt:179cm\n"
	assert create_passports(lines) == [{
		'ecl': 'gry',
		'pid': '860033327',
		'eyr': 2020,
		'hcl': '#fffffd',
		'byr': 1937,
		'iyr': 2017,
		'cid': 147,
		'hgt': '183cm'
	}, {
		'hcl': '#ae17e1',
		'iyr': 2013,
		'eyr': 2024,
		'ecl': 'brn',
		'pid': '760753108',
		'byr': 1931,
		'hgt': '179cm'
	}]

def test_has_all_required_fields():
	# valid
	assert has_all_required_fields({
		'ecl': 'gry',
		'pid': '860033327',
		'eyr': 2020,
		'hcl': '#fffffd',
		'byr': 1937,
		'iyr': 2017,
		'cid': 147,
		'hgt': '183cm'
	})

	# valid
	assert has_all_required_fields({
		'ecl': 'gry',
		'pid': '860033327',
		'eyr': 2020,
		'hcl': '#fffffd',
		'byr': 1937,
		'iyr': 2017,
		'hgt': '183cm'
	})

	# invalid - 7 but has cid
	assert not has_all_required_fields({
		'ecl': 'gry',
		'pid': '860033327',
		'eyr': 2020,
		'hcl': '#fffffd',
		'byr': 1937,
		'iyr': 2017,
		'cid': 147,
	})

	# invalid - less than 8
	assert not has_all_required_fields({
		'ecl': 'gry',
		'pid': '860033327',
		'eyr': 2020,
		'hcl': '#fffffd',
		'byr': 1937,
		'iyr': 2017,
		'cid': 147,
	})

def test_in_range():
	is_valid = in_range(1920, 2002)

	assert not is_valid(1919)
	assert is_valid(1920)
	assert is_valid(2002)
	assert not is_valid(2003)

def test_is_valid_height():
	# invalid height
	assert not is_valid_height('')
	assert not is_valid_height('lfksdj')
	assert not is_valid_height('2020')
	assert not is_valid_height('cm')
	assert not is_valid_height('in')

	# cm: valid and in range
	assert not is_valid_height('149cm')
	assert is_valid_height('150cm')
	assert is_valid_height('193cm')
	assert not is_valid_height('194cm')

	# in: valid and in range
	assert not is_valid_height('58in')
	assert is_valid_height('59in')
	assert is_valid_height('76in')
	assert not is_valid_height('77in')

def test_regex():
	assert regex('^#[0-9a-f]{6}$')('#f0f0f0')

def test_eye_color():
	is_valid_ecl = validators['ecl']

	assert is_valid_ecl('amb')
	assert is_valid_ecl('blu')
	assert is_valid_ecl('brn')
	assert is_valid_ecl('gry')
	assert is_valid_ecl('grn')
	assert is_valid_ecl('hzl')
	assert is_valid_ecl('oth')

	assert not is_valid_ecl('bbb')
	assert not is_valid_ecl('aaa')

if __name__ == "__main__":
    test_create_passport()
    test_create_passports()
    test_has_all_required_fields()
    test_in_range()
    test_is_valid_height()
    test_regex()
    test_eye_color()
