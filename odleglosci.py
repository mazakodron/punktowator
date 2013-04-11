#!/usr/bin/python2
from math import sqrt

def distance(a, b):
	return sqrt((a.real - b.real)**2 + (a.imag - b.imag)**2)

f = open('punkty.txt', 'r')
line = f.readline()

P = complex(0,0)

while line:
	if line.find('START') != -1:
		print line,
	elif line.find('OPUSC') != -1:
		print line,
	elif line.find('PODNIES') != -1:
		print line,
	elif line.find('KONIEC') != -1:
		print line,
	elif line.find('=') == -1:
		x = float(line[:line.find(' ')])
		y = float(line[line.find(' ')+1:-1])
		Pnew = complex(x, y)
		d = distance(P, Pnew)
		print "%f" % d
		P = Pnew
	line = f.readline()
