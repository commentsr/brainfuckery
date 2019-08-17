import sys


class MismatchedBracket(Exception):
	pass


def interpret(program, memsize=30000):
	instruction_pointer = 0
	memory_pointer = 0
	memory = [0]*memsize

	brace_map = {}
	stack = []
	for index, char in enumerate(program):
		if char == "[":
			stack.append(index)
		elif char == "]":
			try:
				prev = stack.pop()
			except IndexError:
				raise MismatchedBracket(f"Unmatched ] at character index {index}") from None
				return
			brace_map[index], brace_map[prev] = prev, index

	if stack:
		raise MismatchedBracket(f"Unmatched [ at character index {stack[0]}") from None

	while instruction_pointer < len(program):
		char = program[instruction_pointer]

		if char == "+":
			memory[memory_pointer] += 1
			if memory[memory_pointer] > 255:
				memory[memory_pointer] = 0

		elif char == "-":
			memory[memory_pointer] -= 1
			if memory[memory_pointer] < 0:
				memory[memory_pointer] = 255

		elif char == ">":
			memory_pointer += 1

		elif char == "<":
			memory_pointer -= 1

		elif char == ".":
			print(
				end=chr(memory[memory_pointer])
			)

		elif char == ",":
			memory[memory_pointer] = ord(sys.stdin.read(1))

		elif char == "[":
			if not memory[memory_pointer]:
				instruction_pointer = brace_map[instruction_pointer]

		elif char == "]":
			instruction_pointer = brace_map[instruction_pointer] - 1

		instruction_pointer += 1


if __name__ == "__main__":
	import os

	if len(sys.argv) > 1:
		if os.path.isfile(sys.argv[1]):
			with open(sys.argv[1], "r") as file:
				program = file.read()
		else:
			program = sys.argv[1]
		interpret(program)
	else:
		print("Usage:\n\tbrainfuck.py {file|program}")
