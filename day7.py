#!/usr/bin/python

"""
--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP addresses (they're IPv7, of course; IPv6 is much too limited). You'd like to figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any four-character sequence which consists of a pair of two different characters followed by the reverse of that pair, such as xyyx or abba. However, the IP also must not have an ABBA within any hypernet sequences, which are contained by square brackets.

For example:

    abba[mnop]qrst supports TLS (abba outside square brackets).
    abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
    aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
    ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?

--- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences (outside any square bracketed sections), and a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet sequences. An ABA is any three-character sequence which consists of the same character twice with a different character between them, such as xyx or aba. A corresponding BAB is the same characters but in reversed positions: yxy and bab, respectively.

For example:

    aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
    xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
    zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).

How many IPs in your puzzle input support SSL?

"""

def breakout(line):
	inners = []
	outers = []
	segment = ''
	idx = 0
	while idx < len(line):
		if line[idx] == '[':
			outers.append(segment)
			segment = ''
			while line[idx] != ']':
				idx += 1
				segment += line[idx]
			inners.append(segment)
			segment = ''
		else:
			segment += line[idx]
		idx += 1
	outers.append(segment)
	return outers, inners
	
def eval_isp(line):
	inner_support = False
	outer_support = False
	segment = ''
	idx = 0
	while idx < len(line):
		if line[idx] == '[':
			outer_support |= supports_tls(segment)
			segment = ''
			while line[idx] != ']':
				idx += 1
				segment += line[idx]
			inner_support |= supports_tls(segment)
			segment = ''
		else:
			segment += line[idx]
		idx += 1
	outer_support |= supports_tls(segment)
	return outer_support and not inner_support

def supports_tls(line):
	idx = 0
	while idx < len(line)-3:
		if line[idx] == line[idx+3] and line[idx+1] == line[idx+2] and line[idx] != line[idx+1]:
			return True
		idx += 1
	return False
	
def supports_ssl(inpt):
	outers, inners = inpt
	for line in outers:
		idx = 0
		while idx < len(line) - 2:
			aba = line[idx:idx+3]
			if aba[0] == aba[2] and aba[0] != aba[1]:
				bab = aba[1]+aba[0]+aba[1]
				for inline in inners:
					if bab in inline:
						return True
			idx += 1
	return False

if __name__ == "__main__":

	# Part 1 and 2 Solution
	tls_count = 0
	ssl_count = 0
	with open("day7_input", "r") as infile:
		for line in infile.readlines():
			if eval_isp(line.strip()):
				tls_count += 1
			if supports_ssl(breakout(line.strip())):
				ssl_count += 1
	print tls_count
	print ssl_count
	
	
			
			
