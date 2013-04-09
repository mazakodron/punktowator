#!/usr/bin/python2
from math import floor
from math import sqrt
from mazakodron import *
from svg.path import *
from sys import argv

def dist2(curve, p, t):
	return (p.real - curve.point(t).real)**2 + (p.imag - curve.point(t).imag)**2

def func(curve, p, t, a):
	return dist2(curve, p, t) - a**2

def distance(a, b):
	return sqrt((a.real - b.real)**2 + (a.imag - b.imag)**2)

def bezier_points(curve, a, eps):
	p = curve.start
	t = 0
	left = 0
	right = 1
	points = []
	#points.append(curve.start)
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
	lastt = curve.point(1)
	d = distance(p, lastt)
	if lastt.imag - p.imag == 0:
		AB = a
	else:
		AB = float(a*abs(lastt.real-p.real))/float(d)
	if lastt.real - p.real == 0:
		BC = a
	else:
		BC = float(AB*abs(lastt.imag - p.imag)) / float(abs(p.real - lastt.real))
	lastx = 0
	lasty = 0

	if(p.real > lastt.real):
		sgn = 1
	else:
		sgn = -1
	lastx = p.real + sgn * AB
	if(p.imag > lastt.imag):
		sgn = 1
	else:
		sgn = -1
	lasty = p.imag + sgn * BC
	last = complex(lastx,lasty)
	points.append(last)

	return points

def line_points(line, a):
	d = distance(line.start, line.end)
	x_diff = 0
	y_diff = 0

	# naprawic odleglosci tutaj bo wychodza jakies popieprzone, np. 18

	if d < a:
		if line.end.imag - line.start.imag == 0:
			x_diff = a
		else:
			x_diff = float(a*abs(line.end.real - line.start.real))/float(d)
		if line.start.real - line.end.real == 0:
			y_diff = a
		else:
			y_diff = float(x_diff * abs(line.end.imag - line.start.imag)) / float(abs(line.start.real - line.end.real))
		d = a
	else:
		x_diff = abs(line.start.real - line.end.real)
		y_diff = abs(line.start.imag - line.end.imag)
		# oblicz z talesa punkt tak, aby przychodzil przez line.start i line.end ale lezal w odleglosci a
		# w innym wypadku licz normalnie x_diff, y_diff
		#
		# rozwazyc przypadek, gdy d < a ale punkty leza w linii prostej
	n = int(floor(float(d)/float(a)))
	#x_diff = abs(line.start.real - line.end.real)
	#y_diff = abs(line.start.imag - line.end.imag)
	
	#if n != 0:
	x_off = float(x_diff)/float(n)
	y_off = float(y_diff)/float(n)
	#else:
	#	x_off = y_off = 0

	# czy to aby na pewno jest dobrze?
	# czy zapewnione jest przejscie o krok a?
	# lol, nope

	x = line.start.real
	y = line.start.imag

	points = []
	sgn_x = 0
	sgn_y = 0
	if (line.start.real < line.end.real):
		sgn_x = 1
	else:
		sgn_x = -1
	if (line.start.imag < line.end.imag):
		sgn_y = 1
	else:
		sgn_y = -1
	
	for i in range(1,n+2):
		points.append(complex(x,y))
		x += sgn_x * x_off
		y += sgn_y * y_off
	#print "a = %(a)d, dist = %(d)f" % {"a" : a, "d":distance(points[0], points[-1])}
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

	uklad wspolrzednych:
	+------> x
	|
	|
	|
	v y

	'''

	# <TEST>
	'''
	p0 = complex(112.3125, 913.29968)
	p1 = complex(512.3125, 912.17468)

	tab = line_points(Line(p0,p1), 25)
	for el in tab:
		print "%(x)f %(y)f" % {"x":el.real, "y":el.imag}
	'''
	# </TEST>
	
	filename = ''
	try:
		filename = argv[1]
	except IndexError:
		raise AssertionError('Brak nazwy pliku')
	a = 10
	eps = 0.001

	mazak = Mazakodron()
	mazak.load(filename)
	#print mazak.getDocDims()
	mazak.loadPaths()
	print "START"
	
	P = complex(0,0)

	for path in mazak.getPaths():
		for el in path:
			#print "P = %f %f" % (P.real, P.imag)
			#print "el = %f %f" % (el.start.real, el.start.imag)
			if P == complex(0,0):
				line = Line(P, complex(el.start.real+mazak.xoffset,el.start.imag+mazak.yoffset))
			else:
				line = Line(P, el.start)
			if line.start != line.end:
				#linepoints = line_points(line, a)
				linepoints = bezier_points(line, a, eps)
				for point in linepoints:
					#if point != line.start:
					print "%(x)f %(y)f" % {"x": point.real, "y":point.imag}
				last = complex(0,0)
				if P == complex(0,0):
					last = complex(linepoints[-1].real-mazak.xoffset,linepoints[-1].imag-mazak.yoffset)
				else:
					last = linepoints[-1]
				mazak.xoffset += last.real - el.start.real
				mazak.yoffset += last.imag - el.start.imag
				
				# tutaj dodac offsety na x i y (mazak.xoffset, mazak.yoffset)
				# i znak w zaleznosci od tego czy pierwotne > nowe czy nie

			print "OPUSC"
			ptype = str(type(el))
			ptype = ptype[ptype.rfind('.')+1:ptype.rfind("'")]
			points = []
			
			if ptype == "CubicBezier":
				#print "Cubic Bezier"
				points = bezier_points(el, a, eps)
				for p in points:
					print "%(x)f %(y)f" % {"x":p.real+mazak.xoffset, "y":p.imag+mazak.yoffset}
				#P = points[-1]
			elif ptype == "QuadraticBezier":
				#print "Quadratic Bezier"
				points = bezier_points(el, a, eps)
				for p in points:
					print "%(x)f %(y)f" % {"x":p.real+mazak.xoffset, "y":p.imag+mazak.yoffset}
				#P = points[-1]
				#print "Quadratic Bezier"
			#elif ptype == "Arc":
			#	print "Arc"
			elif ptype == "Line":
				#print "Line"
				#print "el.start = (%f,%f), el.end = (%f,%f)" % (el.start.real, el.start.imag, el.end.real, el.end.imag)
				#points = []
				if el.start == el.end:
					points = [el.start]
				else:
					points = bezier_points(el, a, eps)
				#points = line_points(el, a)
				for p in points:
					print "%(x)f %(y)f" % {"x":p.real+mazak.xoffset, "y":p.imag+mazak.yoffset}
				#P = points[-1]
			P = points[-1]
			#P = complex(points[-1].real+mazak.xoffset, points[-1].imag+mazak.yoffset)
			#mazak.xoffset += P.real - el.end.real
			#mazak.yoffset += P.imag - el.end.imag
				#print "Line"
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
