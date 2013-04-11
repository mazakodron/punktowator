#!/usr/bin/python2
from math import floor
from math import sqrt
from mazakodron import *
from svg.path import *
from sys import argv

def dist2(curve, p, t):	# odleglosc podniesiona do kwadratu
	return (p.real - curve.point(t).real)**2 + (p.imag - curve.point(t).imag)**2

def func(curve, p, t, a):	# funkcja d^2 - a^2
	return dist2(curve, p, t) - a**2

def distance(a, b):	# odleglosc miedzy punktami a i b
	return sqrt((a.real - b.real)**2 + (a.imag - b.imag)**2)

def bezier_points(curve, a, eps):	# krzywa beziera o danym t, przy dokladnosci a i stalej zaokraglen eps
	p = curve.start	# zaczynamy od poczatku krzywej
	t = 0		# wowczas t = 0
	left = 0	# lewa = 0
	right = 1	# prawa = 0
	points = []	# punkty do zwrocenia
	while t < 1:	# tu zwykla metoda polowienia, kazdy powinien miec na informatyce w liceum. Nie bede sie rozpisywal
		left = t
		right = 1
		while(dist2(curve, p, right) < a**2):
			right *= 2
		olda = None
		oldb = None
		while(abs(func(curve, p, right, a))-eps > 0 and abs(func(curve,p,left-right,a))-eps > 0):
			if olda == abs(func(curve, p, right, a))-eps and oldb == abs(func(curve,p,left-right,a))-eps:
			  # ouch, it's broken
			  break
			olda = abs(func(curve, p, right, a))-eps
			oldb = abs(func(curve,p,left-right,a))-eps
			middle = (right+left)/2.0
			if(func(curve,p,left,a)*func(curve,p,middle,a)<0):
				right = middle
			else:
				left = middle
		t = right
		p = curve.point(t)
		points.append(p)
	lastt = curve.point(1)
	d = distance(p, lastt)		# tu sie zaczyna magia. Jako ze mozemy pozostawic na koncu odcinek o dlugosci (dlugosc_luku mod a), to musimy dorysowac dodatkowy odcinek ktory bedzie szedl przez ostatni wyliczony punkt i punkt konczacy krzywa oraz mial dlugosc 'a'. W tym celu korzystamy z twierdzenia Talesa i podobienstwa trojkatow
	if lastt.imag - p.imag == 0:	# przypadki szczegolne - punkty wspolliniowe
		AB = a
	else:				# tu juz normalny przypadek
		AB = float(a*abs(lastt.real-p.real))/float(d)	# z twierdzenia Talesa
	if lastt.real - p.real == 0:	# kolejny wspomniany przypadek szczegolny
		BC = a
	else:				# ...i znow normalny
		BC = float(AB*abs(lastt.imag - p.imag)) / float(abs(p.real - lastt.real))	# z podobienstwa trojkatow
	lastx = 0
	lasty = 0

	# sgn to znak, ktory okresla po ktorej stronie ma sie znalezc punkt
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

if __name__ == "__main__":
	filename = ''
	try:
		filename = argv[1]
	except IndexError:
		raise AssertionError('Brak nazwy pliku')	# chronimy sie przed zapominalstwem uzytkownikow ;)
	a = 10		# dokladnosc rysowania w milimetrach
	eps = 0.001	# stala zaokraglen numerycznych

	mazak = Mazakodron()
	mazak.load(filename)	# ladujemy plik SVG
	mazak.loadPaths()	# ladujemy sciezki
	print "START"		# start rysowania
	P = complex(0,0)

	for path in mazak.getPaths():	# przerabianie sciezek na punkty
		for el in path:
			# linia od ostatniego punktu do poczatku sciezki - el jest sciezka
			if P == complex(0,0):
				line = Line(P, complex(el.start.real+mazak.xoffset,el.start.imag+mazak.yoffset))
			else:
				line = Line(P, el.start)
			if line.start != line.end:
				linepoints = bezier_points(line, a, eps)
				for point in linepoints:
					print "%(x)f %(y)f" % {"x": point.real, "y":point.imag}
				last = complex(0,0)
				if P == complex(0,0):
					last = complex(linepoints[-1].real-mazak.xoffset,linepoints[-1].imag-mazak.yoffset)
				else:
					last = linepoints[-1]
				# wyrownujemy sciezki tak, aby przesuniecie wynikajace z zaokraglenia trasy przejazdu do wielokrotnosci dokladnosci nie powodowaly bledow przesuniec
				mazak.xoffset += last.real - el.start.real
				mazak.yoffset += last.imag - el.start.imag
			# opusc mazak
			print "OPUSC"
			
			# sprawdz rodzaj sciezki
			ptype = str(type(el))
			ptype = ptype[ptype.rfind('.')+1:ptype.rfind("'")]
			points = []
			
			# wypisz punkt
			if ptype == "CubicBezier":
				points = bezier_points(el, a, eps)
				for p in points:
					print "%(x)f %(y)f" % {"x":p.real+mazak.xoffset, "y":p.imag+mazak.yoffset}
			elif ptype == "QuadraticBezier":
				points = bezier_points(el, a, eps)
				for p in points:
					print "%(x)f %(y)f" % {"x":p.real+mazak.xoffset, "y":p.imag+mazak.yoffset}
			#elif ptype == "Arc":
			#	print "Arc"
			elif ptype == "Line":
				if el.start == el.end:
					points = [el.start]
				else:
					points = bezier_points(el, a, eps)
				for p in points:
					print "%(x)f %(y)f" % {"x":p.real+mazak.xoffset, "y":p.imag+mazak.yoffset}
			else:
				print "PODNIES"
				continue
			# ostatni punkt sciezki staje sie punktem z ktorego przejezdzamy do kolejnego
			P = points[-1]
			# podnies mazak
			print "PODNIES"
	print "KONIEC"
