#!/usr/bin/python

from itertools import permutations
from collections import deque

"""
--- Day 24: Air Duct Spelunking ---

You've finally met your match; the doors that provide access to the roof are locked tight, and all of the controls and related electronics are inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able to interface with some of the exposed wires that have been routed through the HVAC system. If you can direct it to each of those locations, you should be able to bypass the security controls.

You extract the duct layout for this area from some blueprints you acquired and create a map with the relevant locations marked (your puzzle input). 0 is your current location, from which the cleaning robot embarks; the other numbers are (in no particular order) the locations the robot needs to visit at least once each. Walls are marked as #, and open passages are marked as .. Numbers behave like open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########

To reach all of the points of interest as quickly as possible, you would have the robot take the following path:

    0 to 4 (2 steps)
    4 to 1 (4 steps; it can't move diagonally)
    1 to 2 (6 steps)
    2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest route. This path is the fewest steps (in the above example, a total of 14) required to start at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0, what is the fewest number of steps required to visit every non-0 number marked on the map at least once?

--- Part Two ---

Of course, if you leave the cleaning robot somewhere weird, someone is bound to notice.

What is the fewest number of steps required to start at 0, visit every non-0 number marked on the map at least once, and then return to 0?

"""

world = []

def bfs(start, dest):
	search_queue = deque()
	search_queue.append((start, 0))
	seen = set()
	seen.add(start)
	while len(search_queue) > 0:
		posit, steps = search_queue.popleft()
		x, y = posit
		if posit == dest:
			return steps
			
		if x > 0 and (x-1, y) not in seen and world[y][x-1] != '#':
			search_queue.append(((x-1,y), steps + 1))
			seen.add((x-1,y))
		if y > 0 and (x,y-1) not in seen and world[y-1][x] != '#':
			search_queue.append(((x,y-1), steps + 1))
			seen.add((x, y-1))
		if y < len(world)-1 and (x, y+1) not in seen and world[y+1][x] != '#':
			search_queue.append(((x,y+1), steps + 1))
			seen.add((x, y+1))
		if x < len(world[0])-1 and (x+1,y) not in seen and world[y][x+1] != '#':
			search_queue.append(((x+1,y), steps + 1))
			seen.add((x, y+1))
	
	return float('inf') # no solution

if __name__ == "__main__":

	# Part 1 Solution
	
	coords = dict()
	stops = []
	adj_matrix = []
	
	short_trip = float('inf')
	
	with open("day24_input", "r") as infile:
		row_num = 0
		for line in infile.readlines():
			world.append(line.strip())
			for col_num, char in enumerate(line.strip()):
				if char >= '0' and char <= '9':
					coords[char] = (col_num, row_num)
			row_num += 1
	
	stops = coords.keys()
	stops = [ int(x) for x in stops ]
	stops.sort()
	for i in range(len(stops)):
		adj_matrix.append([0]*len(stops))
		
	for i in range(len(stops)):
		for j in range(i, len(stops)):
			adj_matrix[j][i] = bfs(coords[str(i)], coords[str(j)])
			adj_matrix[i][j] = adj_matrix[j][i]

	stops.remove(0) # always start from 0	
	for trip in permutations(stops):
		length = 0
		last = 0
		while len(trip) > 0:
			length += adj_matrix[last][trip[0]]
			last = trip[0]
			trip = trip[1:]
		short_trip = min(short_trip, length)
		
	print short_trip
	
	# Part 2 Solution
	
	short_trip = float('inf')
	
	for trip in permutations(stops):
		length = 0
		last = 0
		trip = list(trip) + [0]
		while len(trip) > 0:
			length += adj_matrix[last][trip[0]]
			last = trip[0]
			trip = trip[1:]
		short_trip = min(short_trip, length)
		
	print short_trip
	
		
			
			
