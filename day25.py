#!/usr/bin/python

"""
--- Day 25: Clock Signal ---

You open the door and find yourself on the roof. The city sprawls away from you for miles and miles.

There's not much time now - it's already Christmas, but you're nowhere near the North Pole, much too far to deliver these stars to the sleigh in time.

However, maybe the huge antenna up here can offer a solution. After all, the sleigh doesn't need the stars, exactly; it needs the timing data they provide, and you happen to have a massive signal generator right here.

You connect the stars you have to your prototype computer, connect that to the antenna, and begin the transmission.

Nothing happens.

You call the service number printed on the side of the antenna and quickly explain the situation. "I'm not sure what kind of equipment you have connected over there," he says, "but you need a clock signal." You try to explain that this is a signal for a clock.

"No, no, a clock signal - timing information so the antenna computer knows how to read the data you're sending it. An endless, alternating pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal at the frequency you would need to use for the data from the stars. "There's no way it can! The only antenna we've installed capable of that is on top of a top-secret Easter Bunny installation, and you're definitely not-" You hang up the phone.

You've extracted the antenna's clock signal generation assembunny code (your puzzle input); it looks mostly compatible with code you worked on just recently.

This antenna code, being a signal generator, uses one extra instruction:

    out x transmits x (either an integer or the value of a register) as the next value for the clock signal.

The code takes a value (via register a) that describes the signal to generate, but you're not sure how it's used. You'll have to find the input to produce the right signal through experimentation.

What is the lowest positive integer that can be used to initialize register a and cause the code to output a clock signal of 0, 1, 0, 1... repeating forever?

"""

program = []

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
	
# output the value of the register to an 'antenna'
def out(r, o):
	print regs[r],

# jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.
def jnz(r, o):
	if r in regs:
		if regs[r] != 0:
			if o in regs:
				regs["ip"] += regs[o]-1
			else:
				regs["ip"] += int(o)-1
	elif int(r) != 0:
		if o in regs:
			regs["ip"] += regs[o]-1
		else:
			regs["ip"] += int(o)-1
		
# tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative means backward
def tgl(r, o):
	#If an attempt is made to toggle an instruction outside the program, nothing happens.
	if r in regs:
		dest = regs["ip"] + regs[r]
	else:
		dest = regs["ip"] + int(r)
	if dest >= 0 and dest < len(program):
		program[dest][3] ^= True

if __name__ == "__main__":

	# Part 1 Solution
	
	op = { "cpy" : cpy, "inc" : inc, "dec" : dec, "jnz" : jnz, "tgl" : tgl, "out" : out}
	top= { "cpy" : jnz, "inc" : dec, "dec" : inc, "jnz" : cpy, "tgl" : inc, "out" : out}
	
	with open("day25_input", "r") as infile:
		for line in infile.readlines():
			line = line.split(" ")
			if len(line) < 3 and len(line) > 1:
				line.append(".")
			line = [ x.strip().strip(",") for x in line ]
			line.append(False) # line toggle status
			program.append(line)
	
	regs["a"] = 175
	
	"""
	Program adds 2555 to the input value, then prints the binary representation of the register.	
	1010 1010 1010 = 2730 --> 2730 - 2555 = 175
	"""
	
	while regs["ip"] < len(program)-1:
		regs["ip"] += 1
		#print regs["ip"], program[regs["ip"]], regs
		if program[regs["ip"]][3]: # Toggle flag set
			try:
				top[program[regs["ip"]][0]](program[regs["ip"]][1], program[regs["ip"]][2])
			except:
				print "Skipped instruction", program[regs["ip"]]
		else:
			op[program[regs["ip"]][0]](program[regs["ip"]][1], program[regs["ip"]][2])
