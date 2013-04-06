#!/usr/bin/python2
from math import ceil
from math import sqrt
from mazakodron import *
from svg.path import *

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
	p0 = complex(491.87909, 742.65982)
	p1 = complex(510.69338, 724.2192)
	p2 = complex(517.39227, 706.1286)
	p3 = complex(513.45907, 684.69745)

	c = CubicBezier(p0,p1,p2,p3)
	p = bezier_points(c, 5, 0.001)
	for el in p:
		print str(el)
	
	#print "Hello, world!"
