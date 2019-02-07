#!/usr/bin/python

"""
--- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a slanted glass ceiling. Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some tiger lilies, you manage to decrypt some of the files you extracted from the servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building - it's a collection of buildings in the nearby area. They're all connected by a local monorail, and there's another building not far from here! Unfortunately, being night, the monorail is currently not operating.

You remotely connect to the monorail control systems and discover that the boot sequence expects a password. The password-checking logic (your puzzle input) is easy to extract, but the code it uses is strange: it's assembunny code designed for the new computer you just assembled. You'll have to execute the code and get the password.

The assembunny code you've extracted operates on four registers (a, b, c, and d) that start at 0 and can hold any integer. However, it seems to make use of only a few instructions:

    cpy x y copies x (either an integer or the value of a register) into register y.
    inc x increases the value of register x by one.
    dec x decreases the value of register x by one.
    jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.

The jnz instruction moves relative to itself: an offset of -1 would continue at the previous instruction, while an offset of 2 would skip over the next instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

The above code would set register a to 41, increase its value by 2, decrease its value by 1, and then skip the last dec a (because a is not zero, so the jnz a 2 skips it), leaving register a at 42. When you move past the last instruction, the program halts.

After executing the assembunny code in your puzzle input, what value is left in register a?

--- Part Two ---

As you head down the fire escape to the monorail, you notice it didn't start; register c needs to be initialized to the position of the ignition key.

If you instead initialize register c to be 1, what value is now left in register a?

"""

regs = { "a" : 0, "b" : 0, "c" : 0, "d" : 0, "ip" : -1 }

# cpy x y copies x (either an integer or the value of a register) into register y
def cpy(r, o):
	if r in regs:
		regs[o] = regs[r]
	else:
		regs[o] = int(r)
# inc x increases the value of register x by one.
def inc(r, o):
	regs[r] += 1
	
# dec x decreases the value of register x by one.	
def dec(r, o):
	regs[r] -= 1

# jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.
def jnz(r, o):
	if r in regs:
		if regs[r] != 0:
			regs["ip"] += int(o)-1
	elif int(r) != 0:
		regs["ip"] += int(o)-1
	

if __name__ == "__main__":

	# Part 1 Solution

	program = []
	
	op = { "cpy" : cpy, "inc" : inc, "dec" : dec, "jnz" : jnz }
	
	with open("day12_input", "r") as infile:
		for line in infile.readlines():
			line = line.split(" ")
			if len(line) < 3 and len(line) > 1:
				line.append(".")
			line = [ x.strip().strip(",") for x in line ]
			program.append(line)

	while regs["ip"] < len(program)-1:
		regs["ip"] += 1
		op[program[regs["ip"]][0]](program[regs["ip"]][1], program[regs["ip"]][2])

	print regs["a"]
	
	# Part 2 Solution
	
	regs = { "a" : 0, "b" : 0, "c" : 1, "d" : 0, "ip" : -1 }
	
	while regs["ip"] < len(program)-1:
		regs["ip"] += 1
		op[program[regs["ip"]][0]](program[regs["ip"]][1], program[regs["ip"]][2])

	print regs["a"]
