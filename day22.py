#!/usr/bin/python

from collections import deque

"""
--- Day 22: Grid Computing ---

You gain access to a massive storage cluster arranged in a grid; each storage node is only connected to the four nodes directly adjacent to it (three if the node is on an edge, two if it's in a corner).

You can directly access data only on node /dev/grid/node-x0-y0, but you can perform some limited actions on the other nodes:

    You can get the disk usage of all nodes (via df). The result of doing this is in your puzzle input.
    You can instruct a node to move (not copy) all of its data to an adjacent node (if the destination node has enough space to receive the data). The sending node is left empty after this operation.

Nodes are named by their position: the node named node-x10-y10 is adjacent to nodes node-x9-y10, node-x11-y10, node-x10-y9, and node-x10-y11.

Before you begin, you need to understand the arrangement of data on these nodes. Even though you can only move data between directly connected nodes, you're going to need to rearrange a lot of the data to get access to the data you need. Therefore, you need to work out how you might be able to shift data around.

To do this, you'd like to count the number of viable pairs of nodes. A viable pair is any two nodes (A,B), regardless of whether they are directly connected, such that:

    Node A is not empty (its Used is not zero).
    Nodes A and B are not the same node.
    The data on node A (its Used) would fit on node B (its Avail).

How many viable pairs of nodes are there?

--- Part Two ---

Now that you have a better understanding of the grid, it's time to get to work.

Your goal is to gain access to the data which begins in the node with y=0 and the highest x (that is, the node in the top-right corner).

For example, suppose you have the following grid:

Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%

In this example, you have a storage grid 3 nodes wide and 3 nodes tall. The node you can access directly, node-x0-y0, is almost full. The node containing the data you want to access, node-x2-y0 (because it has y=0 and the highest x value), contains 6 terabytes of data - enough to fit on your node, if only you could make enough space to move it there.

Fortunately, node-x1-y1 looks like it has enough free space to enable you to move some of this data around. In fact, it seems like all of the nodes have enough space to hold any node's data (except node-x0-y2, which is much larger, very full, and not moving any time soon). So, initially, the grid's capacities and connections look like this:

( 8T/10T) --  7T/ 9T -- [ 6T/10T]
    |           |           |
  6T/11T  --  0T/ 8T --   8T/ 9T
    |           |           |
 28T/32T  --  7T/11T --   6T/ 9T

The node you can access directly is in parentheses; the data you want starts in the node marked by square brackets.

In this example, most of the nodes are interchangable: they're full enough that no other node's data would fit, but small enough that their data could be moved around. Let's draw these nodes as .. The exceptions are the empty node, which we'll draw as _, and the very large, very full node, which we'll draw as #. Let's also draw the goal data as G. Then, it looks like this:

(.) .  G
 .  _  .
 #  .  .

The goal is to move the data in the top right, G, to the node in parentheses. To do this, we can issue some commands to the grid and rearrange the data:

    Move data from node-y0-x1 to node-y1-x1, leaving node node-y0-x1 empty:

    (.) _  G
     .  .  .
     #  .  .

    Move the goal data from node-y0-x2 to node-y0-x1:

    (.) G  _
     .  .  .
     #  .  .

    At this point, we're quite close. However, we have no deletion command, so we have to move some more data around. So, next, we move the data from node-y1-x2 to node-y0-x2:

    (.) G  .
     .  .  _
     #  .  .

    Move the data from node-y1-x1 to node-y1-x2:

    (.) G  .
     .  _  .
     #  .  .

    Move the data from node-y1-x0 to node-y1-x1:

    (.) G  .
     _  .  .
     #  .  .

    Next, we can free up space on our node by moving the data from node-y0-x0 to node-y1-x0:

    (_) G  .
     .  .  .
     #  .  .

    Finally, we can access the goal data by moving the it from node-y0-x1 to node-y0-x0:

    (G) _  .
     .  .  .
     #  .  .

So, after 7 steps, we've accessed the data we want. Unfortunately, each of these moves takes time, and we need to be efficient:

What is the fewest number of steps required to move your goal data to node-x0-y0?

"""

def bfs_to_G(map):
	goal = None
	open = None
	seen = set()
	for y, row in enumerate(map):
		for x, char in enumerate(row):
			if char == 'G':
				goal = (x,y)
			elif char == '_':
				open = (x,y)
	if goal == None or open == None:
		return float('inf')
	search_queue = deque()
	search_queue.append((open, 0))
	seen.add(open)
	while len(search_queue) > 0:
		current, steps = search_queue.popleft()
		x, y = current
		if current == goal:
			return steps
		if x > 0 and (x-1, y) not in seen and map[y][x-1] != '#':
			search_queue.append(((x-1, y), steps+1))
			seen.add((x-1, y))
		if x < len(map[0])-1 and (x+1, y) not in seen and map[y][x+1] != '#':
			search_queue.append(((x+1, y), steps+1))
			seen.add((x+1,y))
		if y < len(map)-1 and (x, y+1) not in seen and map[y+1][x] != '#':
			search_queue.append(((x, y+1), steps+1))
			seen.add((x, y+1))
		if y > 0 and (x, y-1) not in seen and map[y-1][x] != '#':
			search_queue.append(((x, y-1), steps+1))
			seen.add((x, y-1))
	return float('inf')
			
def parse_node(line):
	line = ' '.join(line.split())
	line = line.split(' ')
	path, x, y = line[0].split("-")
	return Node(int(x.replace("x",'')),
				int(y.replace("y",'')),
				int(line[1].replace("T",'')),
				int(line[2].replace("T",'')),
				int(line[3].replace("T",'')))	

class Node:

	def __init__(self, x, y, size, used, avail):
		self.x = x
		self.y = y
		self.size = size
		self.used = used
		self.avail= avail

if __name__ == "__main__":

	nodes = []
	
	viable = 0

	# Part 1 Solution
	with open("day22_input", "r") as infile:
		junk = infile.readline()
		junk = infile.readline()
		for line in infile.readlines():
			nodes.append(parse_node(line.strip()))
			
	for i, node in enumerate(nodes):
		for j in range(i, len(nodes)):
			if (node.used != 0 and node.used <= nodes[j].avail) or (nodes[j].used != 0 and nodes[j].used <= node.avail):
				viable += 1
				
	print viable
	
	# Part 2 Solution
	
	map = []
	x_dim = 0
	y_dim = 0
	for node in nodes:
		x_dim = max(x_dim, node.x)
		y_dim = max(y_dim, node.y)
	
	x_dim += 1
	y_dim += 1
	
	for j in range(y_dim):
		map.append(['#'] * x_dim)
		
	for i, node in enumerate(nodes):
		for j in range(i, len(nodes)):
			if (node.used != 0 and node.used <= nodes[j].avail) or (nodes[j].used != 0 and nodes[j].used <= node.avail):
				map[node.y][node.x] = '.'
				map[nodes[j].y][nodes[j].x] = '.'
				
	map[0][x_dim-1] = 'G'
	
	for node in nodes:
		if node.used == 0:
			map[node.y][node.x] = '_'
	
	"""
	# print map
	for row in map:
		print ''.join(row)
	"""
	
	"""
	.....................................G
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	......................................
	.........#############################
	......................................
	.................................._...
	......................................
	"""
	
	## Move the open space to the corner with the Goal
	steps = bfs_to_G(map)
	## Then move the Goal to the (0,0) mark.
	## It takes 5 actions to move the Goal one spot to the left
	## And moving the open space to the goal placed it one 
	## position to the left, out of the corner
	print steps + (len(map[0])-2) * 5
