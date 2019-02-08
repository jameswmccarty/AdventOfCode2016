#!/usr/bin/python

from collections import deque

"""
--- Day 13: A Maze of Twisty Little Cubicles ---

You arrive at the first floor of this new building to discover a much less welcoming environment than the shiny atrium of the last one. Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers (x,y). Each such coordinate is either a wall or an open space. You can't move diagonally. The cube maze starts at 0,0 and seems to extend infinitely toward positive x and y; negative values are invalid, as they represent a location outside the building. You are in a small waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the layout is actually quite logical. You can determine whether a given x,y coordinate will be a wall or an open space using a simple system:

    Find x*x + 3*x + 2*x*y + y + y*y.
    Add the office designer's favorite number (your puzzle input).
    Find the binary representation of that sum; count the number of bits that are 1.
        If the number of bits that are 1 is even, it's an open space.
        If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10, drawing walls as # and open spaces as ., the corner of the building containing 0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###

Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###

Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?

--- Part Two ---

How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?

Your puzzle input is still 1358.

"""

favorite = 0

# Return True if open or False if wall
def pop_square(x, y):
	global favorite
	value = x*x + 3*x + 2*x*y + y + y*y + favorite
	popcount = 0
	while value > 0:
		if value & 0x01 == 0x01:
			popcount += 1
		value = value >> 1
	if popcount % 2 == 0:
		return True
	return False
	
# Perform a breadth first search.  Return number of steps to destination
# We begin at location (1,1)
def bfs(dest_x, dest_y):
	search_queue = deque()
	seen = set()
	search_queue.append(((1,1),0))
	while len(search_queue) > 0:
		posit, steps = search_queue.popleft()
		x, y = posit
		if x == dest_x and y == dest_y:
			return steps
		seen.add(posit)

		if x > 0 and (x-1,y) not in seen and pop_square(x-1,y):
			search_queue.append(((x-1,y), steps+1))
		if y > 0 and (x,y-1) not in seen and pop_square(x,y-1):
			search_queue.append(((x,y-1), steps+1))
		if (x,y+1) not in seen and pop_square(x,y+1):
			search_queue.append(((x,y+1),steps+1))
		if (x+1,y) not in seen and pop_square(x+1,y):
			search_queue.append(((x+1,y),steps+1))
	
	return float('inf') # no solution

# Perform a breadth first search.  Return number of reachable locations within a given max number of steps.
def area_count(max_steps):
	search_queue = deque()
	seen = set()
	search_queue.append(((1,1),0))
	while len(search_queue) > 0:
		posit, steps = search_queue.popleft()
		x, y = posit
		seen.add(posit)

		if x > 0 and (x-1,y) not in seen and pop_square(x-1,y) and steps < max_steps:
			search_queue.append(((x-1,y), steps+1))
		if y > 0 and (x,y-1) not in seen and pop_square(x,y-1) and steps < max_steps:
			search_queue.append(((x,y-1), steps+1))
		if (x,y+1) not in seen and pop_square(x,y+1) and steps < max_steps:
			search_queue.append(((x,y+1),steps+1))
		if (x+1,y) not in seen and pop_square(x+1,y) and steps < max_steps:
			search_queue.append(((x+1,y),steps+1))
	
	return len(seen)
	
if __name__ == "__main__":

	# Part 1 Solution
	
	# favorite = 10
	# print bfs(7,4)
	
	favorite = 1358
	print bfs(31,39)
	
	# Part 2 Solution
	print area_count(50)
