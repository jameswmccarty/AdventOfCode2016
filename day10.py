#!/usr/bin/python

"""

--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two microchips, and once it does, it gives each one to a different bot or puts it in a marked "output" bin. Sometimes, bots take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single number; the bots must use some logic to decide what to do with each chip. You access the local control computer and download the bots' instructions (your puzzle input).

Some of the instructions specify that a specific-valued microchip should be given to a specific bot; the rest of the instructions indicate what a given bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

    Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
    Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
    Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
    Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a value-2 microchip, and output bin 2 contains a value-3 microchip. In this configuration, bot number 2 is responsible for comparing value-5 microchips with value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips with value-17 microchips?

--- Part Two ---

What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?

"""

outputs = dict() # key = number, value = [ ints ]
bots = dict()

class Bot:

	def __init__(self, identity, lowpass, highpass):
		self.identity = identity
		self.num = int(identity)
		self.lowpass = lowpass # ('bot' | 'output', #) tuple
		self.highpass = highpass # ('bot' | 'output', #) tuple
		self.has = []
		self.had = []
		
	def value_pass(self, input):
		int_input = int(input)
		self.has.append(int_input)
		if len(self.has) >= 2:
			while len(self.has) > 0:
				item1 = self.has.pop()
				item2 = self.has.pop()
				self.had.append(item1)
				self.had.append(item2)
				if self.lowpass[0] == 'bot':
					bots[self.lowpass[1]].value_pass(min(item1, item2))
				else:
					outputs[self.lowpass[1]].append(min(item1, item2))
				if self.highpass[0] == 'bot':
					bots[self.highpass[1]].value_pass(max(item1, item2))
				else:
					outputs[self.highpass[1]].append(max(item1, item2))					
			
		

if __name__ == "__main__":

	# Part 1 Solution
	
	# First pass builds bots with rules
	with open("day10_input", "r") as infile:
		for line in infile.readlines():
			if 'gives' in line: # contains new bot with rules
				line = line.split(" ")
				new_bot = Bot(line[1], (line[5], line[6]), (line[10], line[11].strip()))
				bots[new_bot.identity] = new_bot
				if line[5] == 'output': # pass off to 'output' not 'bot'
					outputs[line[6]] = []
				if line[10] == 'output':
					outputs[line[11].strip()] = []

	# Second pass distributes values to bots
	with open("day10_input", "r") as infile:
		for line in infile.readlines():
			if 'value' in line:
				line = line.split(" ")
				bots[line[5].strip()].value_pass(int(line[1]))
				
	for bot in bots:
		if 61 in bots[bot].had and 17 in bots[bot].had:
			print bot

	# Part 2 Solution
	print outputs['0'][0] * outputs['1'][0] * outputs['2'][0]
