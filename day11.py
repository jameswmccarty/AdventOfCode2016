#!/usr/bin/python

import itertools
from collections import deque

"""
--- Day 11: Radioisotope Thermoelectric Generators ---

You come upon a column of four floors that have been entirely sealed off from the rest of the building except for a small dedicated lobby. There are some radiation warnings and a big sign which reads "Radioisotope Testing Facility".

According to the project status board, this facility is currently being used to experiment with Radioisotope Thermoelectric Generators (RTGs, or simply "generators") that are designed to be paired with specially-constructed microchips. Basically, an RTG is a highly radioactive rock that generates electricity through heat.

The experimental RTGs have poor radiation containment, so they're dangerously radioactive. The chips are prototypes and don't have normal radiation shielding, but they do have the ability to generate an electromagnetic radiation shield when powered. Unfortunately, they can only be powered by their corresponding RTG. An RTG powering a microchip is still dangerous to other microchips.

In other words, if a chip is ever left in the same area as another RTG, and it's not connected to its own RTG, the chip will be fried. Therefore, it is assumed that you will follow procedure and keep chips connected to their corresponding RTG when they're in the same room, and away from other RTGs otherwise.

These microchips sound very interesting and useful to your current activities, and you'd like to try to retrieve them. The fourth floor of the facility has an assembling machine which can make a self-contained, shielded computer for you to take with you - that is, if you can bring it all of the RTGs and microchips.

Within the radiation-shielded part of the facility (in which it's safe to have these pre-assembly RTGs), there is an elevator that can move between the four floors. Its capacity rating means it can carry at most yourself and two RTGs or microchips in any combination. (They're rigged to some heavy diagnostic equipment - the assembling machine will detach it for you.) As a security measure, the elevator will only function if it contains at least one RTG or microchip. The elevator always stops on each floor to recharge, and this takes long enough that the items within it and the items on that floor can irradiate each other. (You can prevent this if a Microchip and its Generator end up on the same floor in this way, as they can be connected while the elevator is recharging.)

You make some notes of the locations of each component of interest (your puzzle input). Before you don a hazmat suit and start moving things around, you'd like to have an idea of what you need to do.

When you enter the containment area, you and the elevator will start on the first floor.

For example, suppose the isolated area has the following arrangement:

The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.

As a diagram (F# for a Floor number, E for Elevator, H for Hydrogen, L for Lithium, M for Microchip, and G for Generator), the initial state looks like this:

F4 .  .  .  .  .  
F3 .  .  .  LG .  
F2 .  HG .  .  .  
F1 E  .  HM .  LM 

Then, to get everything up to the assembling machine on the fourth floor, the following steps could be taken:

    Bring the Hydrogen-compatible Microchip to the second floor, which is safe because it can get power from the Hydrogen Generator:

    F4 .  .  .  .  .  
    F3 .  .  .  LG .  
    F2 E  HG HM .  .  
    F1 .  .  .  .  LM 

    Bring both Hydrogen-related items to the third floor, which is safe because the Hydrogen-compatible microchip is getting power from its generator:

    F4 .  .  .  .  .  
    F3 E  HG HM LG .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  LM 

    Leave the Hydrogen Generator on floor three, but bring the Hydrogen-compatible Microchip back down with you so you can still use the elevator:

    F4 .  .  .  .  .  
    F3 .  HG .  LG .  
    F2 E  .  HM .  .  
    F1 .  .  .  .  LM 

    At the first floor, grab the Lithium-compatible Microchip, which is safe because Microchips don't affect each other:

    F4 .  .  .  .  .  
    F3 .  HG .  LG .  
    F2 .  .  .  .  .  
    F1 E  .  HM .  LM 

    Bring both Microchips up one floor, where there is nothing to fry them:

    F4 .  .  .  .  .  
    F3 .  HG .  LG .  
    F2 E  .  HM .  LM 
    F1 .  .  .  .  .  

    Bring both Microchips up again to floor three, where they can be temporarily connected to their corresponding generators while the elevator recharges, preventing either of them from being fried:

    F4 .  .  .  .  .  
    F3 E  HG HM LG LM 
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Bring both Microchips to the fourth floor:

    F4 E  .  HM .  LM 
    F3 .  HG .  LG .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Leave the Lithium-compatible microchip on the fourth floor, but bring the Hydrogen-compatible one so you can still use the elevator; this is safe because although the Lithium Generator is on the destination floor, you can connect Hydrogen-compatible microchip to the Hydrogen Generator there:

    F4 .  .  .  .  LM 
    F3 E  HG HM LG .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Bring both Generators up to the fourth floor, which is safe because you can connect the Lithium-compatible Microchip to the Lithium Generator upon arrival:

    F4 E  HG .  LG LM 
    F3 .  .  HM .  .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Bring the Lithium Microchip with you to the third floor so you can use the elevator:

    F4 .  HG .  LG .  
    F3 E  .  HM .  LM 
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

    Bring both Microchips to the fourth floor:

    F4 E  HG HM LG LM 
    F3 .  .  .  .  .  
    F2 .  .  .  .  .  
    F1 .  .  .  .  .  

In this arrangement, it takes 11 steps to collect all of the objects at the fourth floor for assembly. (Each elevator stop counts as one step, even if nothing is added to or removed from it.)

In your situation, what is the minimum number of steps required to bring all of the objects to the fourth floor?

--- Part Two ---

You step into the cleanroom separating the lobby from the isolated area and put on the hazmat suit.

Upon entering the isolated containment area, however, you notice some extra parts on the first floor that weren't listed on the record outside:

    An elerium generator.
    An elerium-compatible microchip.
    A dilithium generator.
    A dilithium-compatible microchip.

These work just like the other generators and microchips. You'll have to get them up to assembly as well.

What is the minimum number of steps required to bring all of the objects, including these four new ones, to the fourth floor?

"""

# Return True if all components are on the 4th floor
def move_complete(items):
	#if items.values().count(3) != len(items):
	for item in set(items.values()):
		if item != 3:
			return False
	return True

# Return true if a microchip is on a floor with a generator
# that it is not paired with	
def fried(items):
	for i in range(4):
		floor = [ x for x in items if items[x] == i ]
		if len([ x for x in floor if x[1] == 'G' ]) > 0:
			for component in floor:
				if component[1] == 'M' and component[0]+'G' not in floor:
						return True
	return False

# return only legal move tuples ( no unmatched generators and microchips )
# The first letters must match if the second letters do not
"""
  Integrated into bfs_move_solve
"""
def legal_moves(moves):
	return [ x for x in moves if not (x[0][1] != x[1][1] and x[0][0] != x[1][0]) ]
	
def bfs_move_solve(start):
	seen = set()
	search_queue = deque()
	seen.add(frozenset(start.items()))
	search_queue.append((start, 0))
	while len(search_queue) > 0:
		items, steps = search_queue.popleft()
		elev_floor = items.pop('floor')
		if move_complete(items):
			return steps
			
		"""
		#
		# Below section only runs if we have not found a solution yet.
		#
		"""
		
		# We can move anything on the floor with the elevator
		moveable_items = [ x for x in items if items[x] == elev_floor ]
		# We must move either 1 or 2 items
		base_poss =  moveable_items
		base_poss += [ x for x in itertools.combinations(moveable_items, 2) if not (x[0][1] != x[1][1] and x[0][0] != x[1][0]) ]
		if elev_floor < 3: # not on top floor
			for move in base_poss:
				next_items = dict(items)
				if type(move) == tuple:
					for step in move:
						next_items[step] = elev_floor + 1
				else:
					next_items[move] = elev_floor + 1
				next_items['floor'] = elev_floor + 1
				if frozenset(next_items.items()) not in seen and not fried(next_items):
					seen.add(frozenset(next_items.items())) # prevent back-tracking
					search_queue.append((next_items, steps+1))
		if elev_floor > 0: # not on bottom floor
			for move in base_poss:
				next_items = dict(items)
				if type(move) == tuple:
					for step in move:
						next_items[step] = elev_floor - 1
				else:
					next_items[move] = elev_floor - 1
				next_items['floor'] = elev_floor - 1
				if frozenset(next_items.items()) not in seen and not fried(next_items):
					seen.add(frozenset(next_items.items())) # prevent back-tracking
					search_queue.append((next_items, steps+1))

	return float('inf') # Did not find a solution
		
if __name__ == "__main__":

	# Part 1 Solution

	components = dict() # [name] = floor	
	components['floor'] = 0 # starting level of the elevator
	
	"""
	# The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
	components['HM'] = 0
	components['LM'] = 0
	# The second floor contains a hydrogen generator.
	components['HG'] = 1
	# The third floor contains a lithium generator.
	components['LG'] = 2
	# The fourth floor contains nothing relevant.
	"""
	
	# The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
	components['SG'] = 0
	components['SM'] = 0
	components['PG'] = 0
	components['PM'] = 0
	# The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
	components['TG'] = 1
	components['RG'] = 1
	components['RM'] = 1
	components['CG'] = 1
	components['CM'] = 1
	# The third floor contains a thulium-compatible microchip.
	components['TM'] = 2
	# The fourth floor contains nothing relevant.

	print bfs_move_solve(components)
	"""
	# Part 2 Input
	
	components = dict() # reset	
	components['floor'] = 0
	components['SG'] = 0
	components['SM'] = 0
	components['PG'] = 0
	components['PM'] = 0
	components['TG'] = 1
	components['RG'] = 1
	components['RM'] = 1
	components['CG'] = 1
	components['CM'] = 1
	components['TM'] = 2
	components['EG'] = 0 # Added for part 2
	components['EM'] = 0
	components['DG'] = 0
	components['DM'] = 0

	# Too slow to solve
	print bfs_move_solve(components)
	"""