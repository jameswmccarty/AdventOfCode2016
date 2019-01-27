#!/usr/bin/python

"""
--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an implementation of two-factor authentication after a long game of requirements telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a nearby desk). Then, it displays a code on a little screen, and you type that code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken everything apart and figured out how it works. Now you just have to work out what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for the screen; these instructions are your puzzle input. The screen is 50 pixels wide and 6 pixels tall, all of which start off, and is capable of three somewhat peculiar operations:

    rect AxB turns on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall.
    rotate row y=A by B shifts all of the pixels in row A (0 is the top row) right by B pixels. Pixels that would fall off the right end appear at the left end of the row.
    rotate column x=A by B shifts all of the pixels in column A (0 is the left column) down by B pixels. Pixels that would fall off the bottom appear at the top of the column.

For example, here is a simple sequence on a smaller screen:

    rect 3x2 creates a small rectangle in the top-left corner:

    ###....
    ###....
    .......

    rotate column x=1 by 1 rotates the second column down by one pixel:

    #.#....
    ###....
    .#.....

    rotate row y=0 by 4 rotates the top row right by four pixels:

    ....#.#
    ###....
    .#.....

    rotate column x=1 by 1 again rotates the second column down by one pixel, causing the bottom pixel to wrap back to the top:

    .#..#.#
    #.#....
    .#.....

As you can see, this display technology is extremely powerful, and will soon dominate the tiny-code-displaying-screen market. That's what the advertisement on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display: after you swipe your card, if the screen did work, how many pixels should be lit?

To begin, get your puzzle input.

--- Part Two ---

You notice that the screen is only capable of displaying capital letters; in the font it uses, each letter is 5 pixels wide and 6 tall.

After you swipe your card, what code is the screen trying to display?

"""

grid = []
for i in range(6):
	grid.append(['.']*50)
	
def count_on():
	total = 0
	for row in grid:
		total += ''.join(row).count('#')
	return total
	
def print_grid():
	for row in grid:
		print ''.join(row)
	print
	
def parse(line):
	global grid
	if "rect" in line:
		cmd, dim = line.split(" ")
		x, y = dim.split("x") 
		for i in range(int(x)):
			for j in range(int(y)):
				grid[j][i] = '#'
	elif "rotate" in line:
		if "column" in line:
			line = line.replace("rotate column x=", '')
			col, amt = line.split(" by ")
			next_col = ['.'] * len(grid)
			for idx in range(len(next_col)):
				next_col[(idx+int(amt))%len(next_col)] = grid[idx][int(col)]
			for idx in range(len(next_col)):
				grid[idx][int(col)] = next_col[idx]
		elif "row" in line:
			line = line.replace("rotate row y=", '')
			row, amt = line.split(" by ")
			next_row = ['.'] * len(grid[0])
			for idx in range(len(next_row)):
				next_row[(idx+int(amt))%len(next_row)] = grid[int(row)][idx]
			for idx in range(len(next_row)):
				grid[int(row)][idx] = next_row[idx]		
	
if __name__ == "__main__":

	# Part 1 and 2 Solution
	with open("day8_input", "r") as infile:
		for line in infile.readlines():
			parse(line.strip())
			#print_grid()
	print count_on()
	print_grid()
	
	
