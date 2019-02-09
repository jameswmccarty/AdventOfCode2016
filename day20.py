#!/usr/bin/python

"""
--- Day 20: Firewall Rules ---

You'd like to set up a small hidden computer here so you can use it to get back into the network later. However, the corporate firewall only allows communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems to be messy and poorly maintained, and it's not clear which IPs are allowed. Also, rather than being written in dot-decimal notation, they are written as plain 32-bit integers, which can have any value from 0 through 4294967295, inclusive.

For example, suppose only the values 0 through 9 were valid, and that you retrieved the following blacklist:

5-8
0-2
4-7

The blacklist specifies ranges of IPs (inclusive of both the start and end value) that are not allowed. Then, the only IPs that this firewall allows are 3 and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle input), what is the lowest-valued IP that is not blocked?

--- Part Two ---

How many IPs are allowed by the blacklist?

"""

class Range:

	def __init__(self, low, high):
		self.low = low
		self.high = high
		
	def includes(self, low_val, high_val):
		if self.low <= low_val <= self.high or self.low <= high_val <= self.high:
			return True
		return False
		
	def grow(self, low_val, high_val):
		self.low = min(self.low, low_val)
		self.high = max(self.high, high_val)


if __name__ == "__main__":

	# Part 1 Solution
	
	ranges = []
	
	with open("day20_input", "r") as infile:
		for line in infile.readlines():
			line = line.strip().split("-")
			low = int(line[0])
			high = int(line[1])
			contained = False
			for range in ranges:
				if range.includes(low, high):
					range.grow(low, high)
					contained = True
			if not contained:
				ranges.append(Range(low, high))			
			
	low_addr = 0
	
	while True:
		valid = True
		for range in ranges:
			if range.includes(low_addr, low_addr):
				low_addr = range.high + 1
				valid = False
				break
		if valid:
			break
	print low_addr
			
	# Part 2 Solution

	valid_count = 0
	current_addr = 0
	while current_addr < 4294967295:
		valid = True
		for range in ranges:
			if range.includes(current_addr,current_addr):
				current_addr = range.high + 1
				valid = False
				break
		if valid:
			valid_count += 1
			current_addr += 1
			
	print valid_count
	
