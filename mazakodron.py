from svg.path import *
import xml.etree.ElementTree as et

class Mazakodron:
	scaleFactor = float(1.0)
	sheetWidth = 0
	sheetHeight = 0
	docWidth = 0
	docHeight = 0
	tree = None
	paths = []
	xoffset = 0
	yoffset = 0

	def __init__(self, paperFormat = 'A4', filename=None):
		if(filename != None):
			self.load(filename)
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

	def load(self, svgFile):
		try:
			self.tree = et.parse(svgFile)
			"""
			elements = []
			for el in tree.getroot().findall('.//'):
				if el.tag.find('path') != -1:
					elements.append(el)
			paths = list(parse_path(el.get('d')) for el in elements)
			"""
			self.docWidth = int(self.tree.getroot().get('width'))
			self.docHeight = int(self.tree.getroot().get('height'))
			if self.docWidth > self.docHeight:
				self.sheetWidth, self.sheetHeight = self.sheetHeight, self.sheetWidth
			'''print float(self.sheetWidth)/float(self.docWidth)
			print float(self.sheetHeight)/float(self.docHeight)'''
			self.scaleFactor = min(float(self.sheetWidth)/float(self.docWidth), float(self.sheetHeight)/float(self.docHeight))
			self.docWidth *= self.scaleFactor
			self.docHeight *= self.scaleFactor
			self.xoffset = abs(self.docWidth-self.sheetWidth)/2
			self.yoffset = abs(self.docHeight - self.sheetHeight)/2
			if self.docWidth > self.docHeight:
				self.xoffset,self.yoffset = self.yoffset,self.xoffset
		except (AttributeError, TypeError):
			raise AssertionError('No chyba nie. svgFile powinno byc ciagiem znakow')
	def loadPaths(self):
		elements = []
		for el in self.tree.getroot().findall('.//'):
			if el.tag.find('path') != -1:
				elements.append(el)
		self.paths = list(parse_path(el.get('d')) for el in elements)
		''' przegladac sciezki i dla kazdego punktu *= scaleFactor '''
		for path in self.paths: # skalujemy obraz do wielkosci arkusza po ktorym bedziemy rysowac
			for el in path:
				ptype = str(type(el))
				ptype = ptype[ptype.rfind('.')+1:ptype.rfind("'")]
				el.start *= self.scaleFactor
				el.end *= self.scaleFactor
				if ptype == "CubicBezier":
					#el.start *= scaleFactor
					el.control1 *= self.scaleFactor
					el.control2 *= self.scaleFactor
					#el.end *= scaleFactor
				elif ptype == "QuadraticBezier":
					el.control *= self.scaleFactor
				elif ptype == "Arc":
					el.radius *= scaleFactor
				#print ptype
	def getPaths(self):
		return self.paths
	def getDocDims(self):
		return complex(self.docHeight, self.docWidth)
