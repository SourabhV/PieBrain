#! /usr/bin/python

import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help='turn on debug mode', action='store_true')
parser.add_argument('bffile')
args = parser.parse_args()

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
			try:
				openbrace = bracestack.pop()
			except IndexError:
				bracemap[-1] = -1
				return bracemap
			bracemap[openbrace], bracemap[position] = position, openbrace
	if bracestack:
		bracemap[-1] = -1
	return bracemap

def debugcode(code, codeptr, arrdata):
	print ('Data at arrayptr: %s') % arrdata
	print (''.join(code))
	print (''.join([' ' for x in range(codeptr)]) +  '^\n')

def execute(code, debug):
	bracemap = makebracemap(code)
	try:
		if bracemap[-1] == -1:
			print ('SyntaxError: [ and ] mismatch')
			return
	except KeyError:
		pass

	inputstring = input('Enter input string: ')
	mininplen = len([x for x in code if x == ','])
	if len(inputstring) < mininplen:
		print ('Input string too short. Required length: %d') % mininplen
		return

	array, arrayptr, codeptr, inputptr = [0], 0, 0, 0

	if debug:
		outputstring = ''

	while codeptr < len(code):
		if debug:
			debugcode(code, codeptr, chr(array[arrayptr]))
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
			if debug: outputstring += chr(array[arrayptr])
			else: sys.stdout.write(chr(array[arrayptr]))

		elif operator == '[' and array[arrayptr] == 0:
			codeptr = bracemap[codeptr]

		elif operator == ']' and array[arrayptr] != 0:
			codeptr = bracemap[codeptr]

		codeptr += 1
	if debug: print (outputstring)
	else: print ('')

def main():
	try:
		with open(args.bffile, 'r') as f:
			code = f.read()
			code = [x for x in list(code) if x in ',.<>+-[]']
		execute(code, debug=args.debug)
	except IOError:
		print ('No such file or directory: \'%s\'') % args.bffile

if __name__ == '__main__':
	main()
