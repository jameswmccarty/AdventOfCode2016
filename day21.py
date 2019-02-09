#!/usr/bin/python

"""
--- Day 21: Scrambled Letters and Hash ---

The computer system you're breaking into uses a weird scrambling function to store its passwords. It shouldn't be much trouble to create your own scrambled password so you can add it to the system; you just have to implement the scrambler.

The scrambling function is a series of operations (the exact list is provided in your puzzle input). Starting with the password to be scrambled, apply each operation in succession to the string. The individual operations behave as follows:

    swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
    swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
    rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
    rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
    reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
    move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.

For example, suppose you start with abcde and perform the following operations:

    swap position 4 with position 0 swaps the first and last letters, producing the input for the next step, ebcda.
    swap letter d with letter b swaps the positions of d and b: edcba.
    reverse positions 0 through 4 causes the entire string to be reversed, producing abcde.
    rotate left 1 step shifts all letters left one position, causing the first letter to wrap to the end of the string: bcdea.
    move position 1 to position 4 removes the letter at position 1 (c), then inserts it at position 4 (the end of the string): bdeac.
    move position 3 to position 0 removes the letter at position 3 (a), then inserts it at position 0 (the front of the string): abdec.
    rotate based on position of letter b finds the index of letter b (1), then rotates the string right once plus a number of times equal to that index (2): ecabd.
    rotate based on position of letter d finds the index of letter d (4), then rotates the string right once, plus a number of times equal to that index, plus an additional time because the index was at least 4, for a total of 6 right rotations: decab.

After these steps, the resulting scrambled password is decab.

Now, you just need to generate a new scrambled password and you can access the system. Given the list of scrambling operations in your puzzle input, what is the result of scrambling abcdefgh?

--- Part Two ---

You scrambled the password correctly, but you discover that you can't actually modify the password file on the system. You'll need to un-scramble one of the existing passwords by reversing the scrambling process.

What is the un-scrambled version of the scrambled password fbgdceah?

"""

# rotate right by index per rules
def rotr(password, key):
	steps = password.index(key)
	if steps >= 4:
		steps += 1
	steps += 1
	steps %= len(password)
	steps = len(password) - steps
	return password[steps:] + password[0:steps]

def parse(line, password):
	new_password = list(password)
	if 'swap' in line:
		line = line.split(" ")
		x = line[2]
		y = line[5]
		if 'position' in line:
			x = int(x)
			y = int(y)
			new_password[y] = password[x]
			new_password[x] = password[y]
			return ''.join(new_password)
		elif 'letter' in line:
			new_password = password.replace(x,'.')
			new_password = new_password.replace(y,x)
			new_password = new_password.replace('.',y)
			return new_password
	elif 'rotate' in line:
		if 'left' in line or 'right' in line:
			line = line.split(" ")
			steps = int(line[-2]) % len(password)
			if 'right' in line:
				steps = len(password) - steps
			return password[steps:] + password[0:steps]
		elif 'position' in line:
			key = line[-1]
			return rotr(password, key)
			#steps = password.index(key)
			#if steps >= 4:
			#	steps += 1
			#steps += 1
			#steps %= len(password)
			#steps = len(password) - steps
			#return password[steps:] + password[0:steps]
	elif 'reverse' in line:
		line = line.split(' ')
		x = int(line[2])
		y = int(line[4])+1
		y = min(y,len(password))
		substr = password[x:y]
		return password[0:x] + substr[::-1] + password[y:]
	elif 'move' in line:
		line = line.split(' ')
		x = int(line[2])
		y = int(line[5])
		inst_char = password[x]
		new_password = password.replace(inst_char,'')
		new_password = list(new_password)
		new_password.insert(y, inst_char)
		return ''.join(new_password)
	else:
		return None

		
# opposite function
def rev_parse(line, password):
	new_password = list(password)
	if 'swap' in line:
		line = line.split(" ")
		x = line[2]
		y = line[5]
		if 'position' in line:
			x = int(x)
			y = int(y)
			new_password[y] = password[x]
			new_password[x] = password[y]
			return ''.join(new_password)
		elif 'letter' in line:
			new_password = password.replace(x,'.')
			new_password = new_password.replace(y,x)
			new_password = new_password.replace('.',y)
			return new_password
	elif 'rotate' in line:
		if 'left' in line or 'right' in line:
			line = line.split(" ")
			steps = int(line[-2]) % len(password)
			if 'left' in line:
				steps = len(password) - steps
			return password[steps:] + password[0:steps]
		elif 'position' in line:
			key = line[-1]
			new_password = password[1:] + password[0]
			while rotr(new_password, key) != password:
				new_password = new_password[1:] + new_password[0]
			return new_password
			#steps = len(password) - 1 - password.index(key)
			#steps %= len(password)
			#if steps <= 4:
			#	steps += 1
			#steps += 1
			#steps %= len(password)
			#return password[steps:] + password[0:steps]
	elif 'reverse' in line:
		line = line.split(' ')
		x = int(line[2])
		y = int(line[4])+1
		y = min(y,len(password))
		substr = password[x:y]
		return password[0:x] + substr[::-1] + password[y:]
	elif 'move' in line:
		line = line.split(' ')
		x = int(line[2])
		y = int(line[5])
		inst_char = password[y]
		new_password = password.replace(inst_char,'')
		new_password = list(new_password)
		new_password.insert(x, inst_char)
		return ''.join(new_password)
	else:
		return None

		
if __name__ == "__main__":

	# Part 1 Solution
	
	#password = 'abcde'
	password = 'abcdefgh'
	instructions = []
	with open("day21_input", "r") as infile:
		for line in infile.readlines():
			instructions.append(line.strip())
			password = parse(line.strip(), password)
			
	print password
	
	# Part 2 Solution
	password = 'fbgdceah'
	while len(instructions) > 0:
		password = rev_parse(instructions.pop(), password)
	print password
	

	
			
	
