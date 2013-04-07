#!/usr/bin/python2
from math import ceil
from math import sqrt
from mazakodron import *
from svg.path import *
from sys import argv

def dist2(curve, p, t):
	return (p.real - curve.point(t).real)**2 + (p.imag - curve.point(t).imag)**2

def func(curve, p, t, a):
	return dist2(curve, p, t) - a**2

def bezier_points(curve, a, eps):
	p = curve.start
	t = 0
	left = 0
	right = 1
	points = []
	
	while t < 1:
		left = t
		right = 1
		while(dist2(curve, p, right) < a**2):
			right *= 2
		while(abs(func(curve, p, right, a))-eps > 0 and abs(func(curve,p,left-right,a))-eps > 0):
			middle = (right+left)/2.0
			if(func(curve,p,left,a)*func(curve,p,middle,a)<0):
				right = middle
			else:
				left = middle
		t = right
		p = curve.point(t)
		points.append(p)
	return points

if __name__ == "__main__":
	'''
	to-do:
	dodawac ostatni punkt na krzywej: skorzystac z metody
	podobnej do aproksymacji punktow na prostej. Dlaczego?
	Dlatego, ze bez tego czasem generuje same punkty poczatkowe
	krzywych. Ew. zrobic tez aproksymacje punktow na elipsie,
	ale to zalezy od tego czy dos w swoim svg podaje elipsy/luki.
	Co do szukania ostatnich punktow - wystarczy poprowadzic prosta
	przez ostatni znaleziony punkt i punkt koncowy krzywej ktory jest
	polozony w odleglosci rownej zadanej dokladnosci od ostatniego
	punktu. Mozna ew. skorzystac (chyba) z tw. Talesa do znalezienia
	tego.
	Oprocz tego dodac zamiane x/y w print na koncu w zaleznosci
	od layoutu: moze byc jakas funkcja printPoints(tab, layout)
	gdzie layout byloby horizontal/vertical
	Dodac tez przesuwanie wzgledem ostatnio znalezionego punktu
	i prowadzenie prostych od ostatnio znalezionego punktu do nastepnego
	aby dystans dzielil sie na rowne odcinki dlugosci a gdzie a jest
	dokladnoscia

	to-do wazne:
	zastanowic sie nad efektem bledow zaokraglen numerycznych -
	- nad ich wplywem na ostateczne rozwiazanie
	'''
	filename = ''
	try:
		filename = argv[1]
	except IndexError:
		raise AssertionError('Brak nazwy pliku')
	mazak = Mazakodron()
	mazak.load(filename)
	#print mazak.getDocDims()
	mazak.loadPaths()
	for path in mazak.getPaths():
		for el in path:
			print "RYSUJ"
			ptype = str(type(el))
			ptype = ptype[ptype.rfind('.')+1:ptype.rfind("'")]

			if ptype == "CubicBezier":
				#print "Cubic Bezier"
				points = bezier_points(el, 2, 0.001)
				for p in points:
					print "%(x)f %(y)f" % {"x":p.real, "y":p.imag}
			elif ptype == "QuadraticBezier":
				print "Quadratic Bezier"
			elif ptype == "Arc":
				print "Arc"
			elif ptype == "Line":
				print "Line"
			print "PODNIES"
	print "KONIEC"
	#p0 = complex(491.87909, 742.65982)
	#p1 = complex(510.69338, 724.2192)
	#p2 = complex(517.39227, 706.1286)
	#p3 = complex(513.45907, 684.69745)

	#c = CubicBezier(p0,p1,p2,p3)
	#p = bezier_points(c, 5, 0.001)
	#for el in p:
	#	print str(el)
	
	#print "Hello, world!"
