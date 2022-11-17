import re


with open("./day07.input") as file:
	data = file.readlines()
	data = [ line.strip() for line in data ]


def part1():
	return get_total_containing("shiny gold", [])


def get_total_containing(color, acc):
	lines = [line for line in data if color in line and not line.startswith(color)]

	if len(lines) == 0:
		return acc

	for line in lines:
		res = line.split(" bag")
		acc.append(res[0])
		get_total_containing(res[0], acc)

	return len(set(acc))


def part2():
	rules = to_rules(data)

	return get_total_bags_in(get_rule_by_name("shiny gold", rules), rules) - 1


def to_rules(lines):
	rules = []
	for line in data:
		bag_type, contents_str = line.split(" bags contain ")

		if contents_str == "no other bags.":
			contents = None
		else:
			contents = []
			for content in contents_str[:-1].split(", "):
				quantity, sub_bag_type = re.search("(\d+) (\w+ \w+)", content).groups()
				contents.append({
					"bag_type": sub_bag_type,
					"quantity": int(quantity)
				})

		rules.append({
			"bag_type": bag_type,
			"contents": contents
		})

	return rules


def get_rule_by_name(name, rules):
	return [rule for rule in rules if rule["bag_type"] == name][0]


def get_total_bags_in(bag, rules):
	contents = bag["contents"]
	if contents is None:
		return 1

	total = 1
	for bag_content in contents:
		bag_type = bag_content["bag_type"]
		qty = bag_content["quantity"]
		inner_bag = get_rule_by_name(bag_type, rules)


		total += qty * get_total_bags_in(inner_bag, rules)

	return total


print(part1())
print(part2())