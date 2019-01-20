#!/usr/bin/python

"""
--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes up this part of Easter Bunny HQ. This must be a graphic design department; the walls are covered in specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes, but... 5 10 25? Some of these aren't triangles. You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side. For example, the "triangle" given above is impossible, because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified in groups of three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?
"""

if __name__ == "__main__":

	# Part 1 Solution
	
	valid = 0
	
	with open("day3_input", "r") as infile:
		for line in infile.readlines():
			sides = line.lstrip().strip().split("  ")
			sides = [int(x) for x in sides if x != '']
			sides.sort()
			if sides[0] + sides[1] > sides[2]:
				valid += 1
	print valid
			
	# Part 2 Solution
	
	valid = 0
	
	with open("day3_input", "r") as infile:
		while True:
			row1 = infile.readline()
			if row1 == '':
				break
			row2 = infile.readline()
			row3 = infile.readline()
			row1 = row1.lstrip().strip().split("  ")
			row2 = row2.lstrip().strip().split("  ")
			row3 = row3.lstrip().strip().split("  ")
			row1 = [int(x) for x in row1 if x != '']
			row2 = [int(x) for x in row2 if x != '']
			row3 = [int(x) for x in row3 if x != '']
		
			for i in range(3):
				tri_poss = [ row1[i], row2[i], row3[i] ]
				tri_poss.sort()
				if tri_poss[0] + tri_poss[1] > tri_poss[2]:
					valid += 1
					
	print valid
			
