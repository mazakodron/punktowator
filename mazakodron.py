from svg.path import *			# do przerabiania sciezek
import xml.etree.ElementTree as et	# do ladowania XMLa z pliku SVG

class Mazakodron:
	scaleFactor = float(1.0)	# wspolczynnik skalowania
	sheetWidth = 0			# szerokosc kartki
	sheetHeight = 0			# wysokosc kartki
	docWidth = 0			# szerokosc dokumentu
	docHeight = 0			# wysokosc dokumentu
	tree = None			# drzewo XML
	paths = []			# sciezki z pliku SVG
	xoffset = 0			# przesuniecie na osi X
	yoffset = 0			# przesuniecie na osi Y

	def __init__(self, paperFormat = 'A4', filename=None):	# konstruktor klasy: domyslnie ustawiamy format kartki na A4
		if(filename != None):
			self.load(filename)
		# dalej sa wymiary w milimetrach kartek o danym formacie
		if paperFormat == 'A5':
			self.sheetWidth = 148
			self.sheetHeight = 210
		elif paperFormat == 'A4':
			self.sheetWidth = 210
			self.sheetHeight = 297
		elif paperFormat == 'A3':
			self.sheetWidth = 297
			self.sheetHeight = 420
		elif paperFormat == 'A2':
			self.sheetWidth = 420
			self.sheetHeight = 594

	def load(self, svgFile):	# zaladuj plik o nazwie svgFile
		try:
			self.tree = et.parse(svgFile)					# wczytaj elementy XML
			self.docWidth = int(self.tree.getroot().get('width'))		# pobierz szerokosc dokumentu
			self.docHeight = int(self.tree.getroot().get('height'))		# pobierz wysokosc dokumentu
			if self.docWidth > self.docHeight:	# "obroc kartke" aby dopasowac do dokumentu
				self.sheetWidth, self.sheetHeight = self.sheetHeight, self.sheetWidth
			
			self.scaleFactor = min(float(self.sheetWidth)/float(self.docWidth), float(self.sheetHeight)/float(self.docHeight))	# oblicz wspolczynnik skalowania
			self.docWidth *= self.scaleFactor			# przeskaluj dokument
			self.docHeight *= self.scaleFactor			# jak wyzej
			self.xoffset = abs(self.docWidth-self.sheetWidth)/2	# wycentruj
			self.yoffset = abs(self.docHeight - self.sheetHeight)/2	# jak wyzej
			if self.docWidth > self.docHeight:	# obroc przesuniecia aby dostosowac do kartki i dokumentu
				self.xoffset,self.yoffset = self.yoffset,self.xoffset
		except (AttributeError, TypeError):
			raise AssertionError('No chyba nie. svgFile powinno byc ciagiem znakow')
	def loadPaths(self):	# zaladuj sciezki
		elements = []	# elementy XML
		for el in self.tree.getroot().findall('.//'):	# pobierz wszystkie elementy
			if el.tag.find('path') != -1:		# jesli element jest sciezka
				elements.append(el)		# to wrzuc go do listy
		self.paths = list(parse_path(el.get('d')) for el in elements)	# utworz liste zawierajaca sciezki w rozumieniu svg.path
		
		for path in self.paths: # skalujemy punkty do rozmiarow arkusza po ktorym bedziemy rysowac
			for el in path:
				ptype = str(type(el))	# pobierz typ ptype
				ptype = ptype[ptype.rfind('.')+1:ptype.rfind("'")]	# wyluskuje nazwe, np. CubicBezier
				el.start *= self.scaleFactor	# przeskaluj
				el.end *= self.scaleFactor	# jak wyzej
				if ptype == "CubicBezier":
					el.control1 *= self.scaleFactor	# tez skalowanie
					el.control2 *= self.scaleFactor	# ...i znowu...
				elif ptype == "QuadraticBezier":
					el.control *= self.scaleFactor	# czy to sie kiedys skonczy?
				elif ptype == "Arc":
					el.radius *= scaleFactor	# tak, to ostatni!
				
	def getPaths(self):	# zwroc liste sciezek
		return self.paths
	def getDocDims(self):	# pobierz rozmiar dokumentu
		return complex(self.docHeight, self.docWidth)
