import sys, os, subprocess

BOILERPLATE = """
#include <stdio.h>
int main ()
{
	char memory[30000];
	int pointer = 0;
	%s
	return 0;
}
"""

INSTRUCTIONS = {
    "+": "++memory[pointer];",
    "-": "--memory[pointer];",
    ">": "++pointer;",
    "<": "--pointer;",
    ".": "putchar(memory[pointer]);",
    ",": "memory[pointer]=getchar();",
    "[": "while(memory[pointer]){",
    "]": "}"
}

def transpile(program):
    c_instructions = []

    for char in program:
        if char in INSTRUCTIONS.keys():
            c_instructions.append(INSTRUCTIONS[char])

    code = BOILERPLATE % "\n\t".join(c_instructions)

    subprocess.Popen(
        "gcc -x c -o transpiled -".split(),
        stdin=subprocess.PIPE
    ).communicate(
        input=bytes(code, "utf-8")
    )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            with open(sys.argv[1], "r") as file:
                program = file.read()
        else:
            program = sys.argv[1]

        transpile(program)
    else:
        print("Usage:\n\ttranspile.py {file|program}")
