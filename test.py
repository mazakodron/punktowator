#!/usr/bin/python2
from math import sqrt

def bezier(p0, p1, p2, p3, t):
	ret = (1-t)**3 * p0 + 3*(1-t)**2 * t * P1 + 3 * (1-t) * t**2 * P2 + t**3 * P3
	return ret

def dist2(p, p0, p1, p2, p3, t):
	ret = (p.real - bezier(p0,p1,p2,p3,t).real)**2 + (p.imag - bezier(p0,p1,p2,p3,t).imag)**2
	return ret

def func(p, p0, p1, p2, p3, t, a):
	return dist2(p,p0,p1,p2,p3,t) - a**2
	


if __name__ == "__main__":
	P0 = complex(491.87909, 742.65982)
	P1 = complex(510.69338, 724.2192)
	P2 = complex(517.39227, 706.1286)
	P3 = complex(513.45907, 684.69745)
	
	P = P0
	lewa = 0
	prawa = 1
	a = 0.1

	while(dist2(P,P0,P1,P2,P3,prawa) < a**2):
		prawa *= 2
	eps = 0.001
	while(abs(func(P,P0,P1,P2,P3,prawa,a)) - eps > 0 and abs(func(P,P0,P1,P2,P3,lewa-prawa,a))-eps > 0):
		srodek = (prawa+lewa)/2.0
		if(func(P,P0,P1,P2,P3,lewa,a)*func(P,P0,P1,P2,P3,srodek,a) < 0):
			prawa = srodek
		else:
			lewa = srodek
	szukany = bezier(P0,P1,P2,P3,prawa)
	print "t = %(t)f" % {"t": prawa}
	print "P = %(x)f,%(y)f" % {"x":szukany.real, "y":szukany.imag}
	d = sqrt(float(P0.real - szukany.real)**2 + float(P0.imag - szukany.imag)**2)
	print "dist(P0,P) = %(d)f" % {"d":d}
