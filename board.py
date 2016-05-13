# -*- coding: utf-8 -*-
import random,copy
from tabulate import tabulate

class Board():
	"""
	Area board model
	"""
	def __init__(self,height,width,colors):
		"""
		create random board with given parameters
		"""

		assert len(colors)	> 1, "colors list too short, length must be > 1"
		assert height     	> 0, "height too small, must be > 0"
		assert width      	> 0, "width too small, must be > 0"

		self.height	= height
		self.width 	= width
		self.colors	= colors
		self.area  	= [[random.randrange(len(colors)) for x in range(width)] \
		           		for x in range(height)]

	def __getitem__(self,key):
		x,y	= key
		return self.area[x][y]

	def __setitem__(self,key,value):
		x,y            	= key
		self.area[x][y]	= value

	def __str__(self):
		return tabulate(self.area)

	def set_start(self,x):
		"""
		set a starting point at `x`
		"""

		assert x[0] in xrange(self.height), "height coordinate out of bound"
		assert x[1] in xrange(self.width), "width coordinate out of bound"

		color = self[x]
		colors = len(self.colors)
		for i in self.get_neighbors(x):
			# set immediate neighbors to same color
			self[i] = color
			n = filter(lambda k: k != x,self.get_neighbors(i))
			for j in n:
				# set 2nd-grade neighbors to different color
				if self[j] == color:
					self[j] = (self[j] + 1) % colors

	def get_neighbors(self,x):
		"""
		return coordinates of neighbors of `x` as list
		"""

		x,y = x

		assert x in xrange(self.height)
		assert y in xrange(self.width)

		dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
		return [(x+a,y+b) for a,b in dirs if \
			all([x+a < self.height,y+b < self.width,x+a >= 0,y+b >= 0])]

	def get_area_with_border(self,x):
		"""
		return coordinates of area of `x` as set and its border as list
		"""

		assert x[0] in xrange(self.height)
		assert x[1] in xrange(self.width)

		# TODO: optimize by saving previous states
		color = self[x]
		todo = set([x])
		area = set()
		border = []

		while todo:
			y = todo.pop()

			area.add(y)

			border +=	filter( \
			         	lambda k: k not in border and \
			         	self[k] != color, \
			         	self.get_neighbors(y))

			todo |=	set(filter( \
			       	lambda k: k not in area and \
			       	self[k] == color, \
			       	self.get_neighbors(y)))

		return area,border

	def get_extended_area_with_border(self,a,b):
		"""
		return coordinates of superset of `a` and its border, using border `b`
		"""

		color = self[next(iter(a))] # pick element from `a` nondestructively
		todo = set(b)
		area = a
		border = []

		# TODO: validate
		while todo:
			y = todo.pop()

			if self[y] == color:
				area.add(y)

				border +=	filter( \
				         	lambda k: k not in border and \
				         	self[k] != color, \
				         	self.get_neighbors(y))

				todo |=	set(filter( \
				       	lambda k: k not in area and \
				       	self[k] == color, \
				       	self.get_neighbors(y)))
			else:
				# if any(filter(lambda x: x in area,self.get_neighbors(y))):
				border.append(y)

		return area,border

	def get_area(self,x):
		return self.get_area_with_border(x)[0]

	def get_border(self,x):
		return self.get_area_with_border(x)[1]


	def set_color(self,x,c):
		"""
		set area around `x` to color `c`
		"""

		assert x[0]	in xrange(self.height)
		assert x[1]	in xrange(self.width)
		assert c   	in xrange(len(self.colors))

		a = self.get_area(x)
		for i in a:
			self[i] = c

	def get_complete_area(self,x):
		"""
		return area of `x` as `True`, border as `False`, `None` else
		"""

		assert x[0] in xrange(self.height)
		assert x[1] in xrange(self.width)

		area = copy.deepcopy(self)
		a,b = area.get_area_with_border(x)
		for i in range(area.height):
			for j in range(area.width):
				if (i,j) in a:
					area[i,j] = True
				elif (i,j) in b:
					area[i,j] = False
				else:
					area[i,j] = None
		return area

	# DEPRECATED

	def set_color_recursive(self,x,c):
		"""
		set area around `x` to color `c`
		"""

		assert x[0] in xrange(self.height)
		assert x[1] in xrange(self.width)
		assert c in xrange(len(self.colors))

		ref    	= self[x]
		self[x]	= c
		for i in self.get_neighbors(x):
			if self[i] == ref:
				self.set_color_recursive(i,c)
