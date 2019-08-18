#include <iostream>
#include <stack>
#include <map>
#include <cstring>
#include <fstream>


void interpret(const char program[], int mem_size) {

	int program_length = std::strlen(program);

	std::map<int,int> brace_map;
	std::stack<int> brace_stack;
	for (int index=0; index < program_length; index++) {
		switch (program[index]) {

			case '[':
				brace_stack.push(index);
				break;

			case ']':
				if (!brace_stack.empty()) {
					int i = brace_stack.top();
					brace_stack.pop();
					brace_map.insert({i, index});
					brace_map.insert({index, i});
				} else {
					std::cout << "Unmatched ] at character index " + std::to_string(index);
					std::cout << std::endl;
					exit(1);
				}
				break;
		}
	}
	if (!brace_stack.empty()) {
		std::cout << "Unmatched [ at character index " + std::to_string(brace_stack.top());
		std::cout << std::endl;
		exit(1);
	}

	char memory[mem_size] = {0};
	int memory_pointer = 0;
	int instruction_pointer = 0;

	while (instruction_pointer < program_length) {
		switch(program[instruction_pointer]) {

			case '+':
				memory[memory_pointer]++;
				break;

			case '-':
				memory[memory_pointer]--;
				break;

			case '>':
				memory_pointer++;
				break;

			case '<':
				memory_pointer--;
				break;

			case '.':
				std::putchar(memory[memory_pointer]);
				break;

			case ',':
				memory[memory_pointer] = std::getchar();
				break;

			case '[':
				if(memory[memory_pointer] == 0) {
					instruction_pointer = brace_map[instruction_pointer];
				}
				break;

			case ']':
				instruction_pointer = brace_map[instruction_pointer]-1;
				break;
		}
		instruction_pointer++;
	}

	std::cout << "\n";
}


int main(int argc, char const *argv[]) {

	if (argc != 2) {
		std::cout << "Usage:\n\tinterpreter {file|program}";
		std::cout << std::endl;
		exit(1);
	}

	std::ifstream file;
	file.open(argv[1], std::ios::in | std::ios::binary);

	if (file) {
		std::string program;
		file >> program;
		file.close();
		interpret(program.c_str(), 30000);
	} else {
		interpret(argv[1], 30000);

	}

	return 0;
}
