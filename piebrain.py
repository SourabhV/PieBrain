import sys

try:
	input = raw_input
except NameError:
	pass

def makebracemap(code):
	bracestack, bracemap = [], {}
	for position, operator in enumerate(code):
		if operator == '[':
			bracestack.append(position)
		elif operator == ']':
			openbrace = bracestack.pop()
			bracemap[openbrace], bracemap[position] = position, openbrace
	return bracemap

def printcode(code, codeptr, s):
	print (''.join(code), '  |  ', s)
	print (''.join([' ' for x in range(codeptr-2)]), '^')

def execute(code):
	inputstring = input('Enter input string: ')
	bracemap = makebracemap(code)

	array, arrayptr, codeptr, inputptr = [0], 0, 0, 0

	while codeptr < len(code):
		# printcode(code, codeptr, array[arrayptr])
		operator = code[codeptr]

		if operator == '>':
			arrayptr += 1
			if arrayptr == len(array):
				array.append(0)

		elif operator == '<':
			arrayptr = 0 if arrayptr == 0 else arrayptr-1

		elif operator == '+':
			array[arrayptr] = array[arrayptr]+1 if array[arrayptr] < 255 else 0

		elif operator == '-':
			array[arrayptr] = array[arrayptr]-1 if array[arrayptr] > 0 else 255

		elif operator == ',':
			array[arrayptr] = ord(inputstring[inputptr])
			inputptr += 1

		elif operator == '.':
			sys.stdout.write(chr(array[arrayptr]))

		elif operator == '[' and array[arrayptr] == 0:
			codeptr = bracemap[codeptr]

		elif operator == ']' and array[arrayptr] != 0:
			codeptr = bracemap[codeptr]

		codeptr += 1

def main():
	if len(sys.argv) == 2:
		with open(sys.argv[1], 'r') as f:
			code = f.read()
			execute([x for x in list(code) if x in ',.<>+-[]'])
	else:
		print ("Usage: python %s filename") % (sys.argv[0])

if __name__ == '__main__':
	main()
