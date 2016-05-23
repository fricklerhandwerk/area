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
		set a starting point at `x`, return starting area
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
		return self.get_area({x},self.get_neighbors(x))

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

	def get_area(self,a,b):
		"""
		Args:
			a	set representing existing area
			b	list representing border of `a`
		Returns:
			area  	set representing larger area that contains `a`
			border	list representing border of `area`
		NOTE:
			to get area around single cell, call
				get_area({x},self.get_neighbors(x))
		"""

		assert b != [], "if border empty, area will not be updated"

		# pick element from `a` nondestructively
		for c in a: color=self[c]; break
		todo = set(b)
		area = a
		border = []

		while todo:
			x = todo.pop()

			if self[x] == color:
				area.add(x)

				border +=	filter( \
				         	lambda k: k not in border and \
				         	self[k] != color, \
				         	self.get_neighbors(x))

				todo |=	set(filter( \
				       	lambda k: k not in area and \
				       	self[k] == color, \
				       	self.get_neighbors(x)))
			else:
				border.append(x)

		return area,border

	def get_enclosed_area(self,a,b,s):
		"""
		Args:
			a	set representing an area
			b	list representing border of `a`
			s	set of coordinates to reach
		Returns:
			area  	set representing area that is enclosed by `a`, i.e.
			      	all coordinates from which one cannot reach any point in `s`
			      	without stepping through `a`
			border	list representing border of `area`
		"""

		todo = set(b) - s	# drop border cells if they belong to other players
		area = set(a)    	# create copy of `a`
		border = list(b) 	# create copy of `b`
		components = []  	# list of enclosed components found

		# check reachability of `s` by picking a border cell
		while todo:
			x = todo.pop()
			# start a new component
			todo2 = {x}
			component = set()
			enclosed = True
			# fill with neighbors not in original area
			# until a cell from `s` is caught or `todo2` empty
			while todo2:
				y = todo2.pop()
				component.add(y)
				n =	set(filter( \
				   	lambda k: k not in area and k not in component, \
				   	self.get_neighbors(y)))
				todo2 |= n
				# `s` reached
				if any(map(lambda x: x in s,n)):
					enclosed = False
					break
			# if anything left, fill component avoiding `s`
			while todo2:
				y = todo2.pop()
				component.add(y)
				todo2 |=	set(filter( \
				        	lambda k: k not in area and \
				        	k not in component and \
				        	k not in s, \
				        	self.get_neighbors(y)))
			if enclosed:
				# add it to enclosed area
				area |= component
				# add to list of components, it's faster to color
				components.append(component)
				# remove component cells from border
				border = filter(lambda x: x not in component,border)
			# shrink search space for next iteration
			todo -= component
		return area,border,components


	def set_color(self,a,c):
		"""
		set area `a` to color `c`
		"""

		assert c in xrange(len(self.colors))

		for x,y in a:
			assert x in xrange(self.height)
			assert y in xrange(self.width)
			self[x,y] = c

	def get_complete_area(self,x):
		"""
		return area of `x` as `True`, border as `False`, `None` else
		"""

		assert x[0] in xrange(self.height)
		assert x[1] in xrange(self.width)

		area = copy.deepcopy(self)
		a,b = area.get_area({x},self.get_neighbors(x))
		for i in range(area.height):
			for j in range(area.width):
				if (i,j) in a:
					area[i,j] = True
				elif (i,j) in b:
					area[i,j] = False
				else:
					area[i,j] = None
		return area

