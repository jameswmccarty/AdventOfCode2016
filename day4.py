#!/usr/bin/python

"""
--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of course, the list is encrypted and full of decoy data, but the instructions to decode the list are barely hidden nearby. Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. For example:

    aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are a (5), b (3), and then a tie between x, y, and z, which are listed alphabetically.
    a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each), the first five are listed alphabetically.
    not-a-real-room-404[oarel] is a real room.
    totally-real-room-200[decoy] is not.

Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?

--- Part Two ---

With all the decoy data out of the way, it's time to decrypt this list and get moving.

The room names are encrypted by a state-of-the-art shift cipher, which is nearly unbreakable without the right software. However, the information kiosk designers at Easter Bunny HQ were not expecting to deal with a master cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet a number of times equal to the room's sector ID. A becomes B, B becomes C, Z becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

What is the sector ID of the room where North Pole objects are stored?

"""

def validate(room, checksum):
	letters = dict()
	for segment in room:
		for char in segment:
			if char in letters:
				letters[char] += 1
			else:
				letters[char] = 1
	comp = [ x[0] for x in sorted(sorted(letters.items(), key=lambda a:a[0]), key=lambda b:b[1], reverse=True) ][0:5]
	if ''.join(comp) == checksum:
		return True
	return False

def decode(room, shift):
	out = ''
	for segment in room:
		for char in segment:
			val = ord(char)-97
			val += (shift % 26)
			val %= 26
			out += chr(val+97)
		out += ' '
	#print out
	return out
	
	
if __name__ == "__main__":

	# Part 1 Solution
	
	total = 0
	
	with open("day4_input", "r") as infile:
		for line in infile.readlines():
			room, checksum = line.split("[")
			checksum = checksum.replace("]", '').strip()
			segments = room.split("-")
			sector_ID = int(segments[-1])
			segments = segments[:-1]
			if validate(segments, checksum):
				total += sector_ID
				
	print total
	
	# Part 2 Solution
	with open("day4_input", "r") as infile:
		for line in infile.readlines():
			room, checksum = line.split("[")
			checksum = checksum.replace("]", '').strip()
			segments = room.split("-")
			sector_ID = int(segments[-1])
			segments = segments[:-1]
			if validate(segments, checksum):
				soln = decode(segments, sector_ID)
				if "north" in soln and "pole" in soln:
					print soln, sector_ID
	
