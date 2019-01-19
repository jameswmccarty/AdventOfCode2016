#!/usr/bin/python

"""
--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by stars. Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get - the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North. Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the destination?

For example:

    Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
    R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
    R5, L5, R5, R3 leaves you 12 blocks away.

How many blocks away is Easter Bunny HQ?

--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?

"""

if __name__ == "__main__":

	# 0 - North
	# 1 - East
	# 2 - South
	# 3 - West
	dir_idx = 0
	dirs = [1, 1, -1, -1]
	vert = 0
	horiz = 0

	# Part 1 Solution
	with open("day1_input", "r") as infile:
		directions = infile.read().strip().split(",")
	for step in directions:
		if "R" in step:
			dir_idx += 1
			dir_idx %= 4
			step = int(step.replace("R",''))
		else:
			dir_idx -= 1
			dir_idx %= 4
			step = int(step.replace("L",''))
		if dir_idx % 2 == 0:
			vert += dirs[dir_idx]*step
		else:
			horiz += dirs[dir_idx]*step
	print abs(vert)+abs(horiz)
	
	# Part 2 Solution
	seen = set()
	last = (0,0)
	seen.add(last)
	for step in directions:
		if "R" in step:
			dir_idx += 1
			dir_idx %= 4
			step = int(step.replace("R",''))
		else:
			dir_idx -= 1
			dir_idx %= 4
			step = int(step.replace("L",''))
		if dir_idx % 2 == 0:
			for i in range(step):
				next = (last[0]+dirs[dir_idx], last[1])
				if next in seen:
					print abs(next[0])+abs(next[1])
					exit()
				seen.add(next)
				last = next
		else:
			for i in range(step):
				next = (last[0], last[1]+dirs[dir_idx])
				if next in seen:
					print abs(next[0])+abs(next[1])
					exit()
				seen.add(next)
				last = next
