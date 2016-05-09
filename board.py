# -*- coding: utf-8 -*-
import random,copy
from tabulate import tabulate
from IPython import embed

class Board():
	"""
	Area board model
	"""
	def __init__(self,width,height,colors):
		"""
		create random board with given parameters
		"""

		assert len(colors)	> 1, "colors list too short, length must be > 1"
		assert width      	> 0, "width too small, must be > 0"
		assert height     	> 0, "height too small, must be > 0"

		self.width 	= width
		self.height	= height
		self.colors	= colors
		self.area  	= [[random.randint(0,len(colors)-1) for x in range(width)] \
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

		for i in self.get_neighbors(x):
			# set immediate neighbors to same color
			self[i] = self[x]
			for j in filter(lambda k: k != x,self.get_neighbors(i)):
				# set 2nd-grade neighbors to different color
				if self[j] == self[x]:
					self[j] = (self[j] + 1) % len(self.colors)

	def get_neighbors(self,x):
		"""
		return coordinates of neighbors of `x` as list
		"""

		assert x[0] in xrange(self.height)
		assert x[1] in xrange(self.width)

		x,y = x
		dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
		return [	[x+a,y+b] for a,b in dirs if \
		        	all([x+a < self.height,y+b < self.width,x+a >= 0,y+b >= 0])]

	def get_area(self,x):
		"""
		return coordinates of area of `x` and its border
		"""

		assert x[0] in xrange(self.height)
		assert x[1] in xrange(self.width)

		# TODO: optimize by saving previous states
		todo = [x]
		area = []
		border = []

		while todo != []:
			y = todo[0]

			area.append(y)

			border +=	filter( \
			         	lambda k: k not in border and \
			         	self[k] != self[x], \
			         	self.get_neighbors(y))

			todo = todo[1:]
			todo +=	filter( \
			       	lambda k: k not in area and \
			       	self[k] == self[x], \
			       	self.get_neighbors(y))

		return area,border

	def set_color(self,x,c):
		"""
		set area around `x` to color `c`
		"""

		assert x[0] in xrange(self.height)
		assert x[1] in xrange(self.width)
		assert c in xrange(len(self.colors))

		a,_ = self.get_area(x)
		for i in a:
			self[i] = c

	def get_complete_area(self,x):
		"""
		return area of `x` as `True`, border as `False`, `None` else
		"""

		assert x[0] in xrange(self.height)
		assert x[1] in xrange(self.width)

		area = copy.deepcopy(self)
		a,b = area.get_area(x)
		for i in range(area.height):
			for j in range(area.width):
				if [i,j] in a:
					area[i,j] = True
				elif [i,j] in b:
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

def main():
	"""
	just for testing
	"""

	HEIGHT = 5
	WIDTH = 10
	colors = ["red","green","blue","yellow","magenta"]

	a = Board(WIDTH,HEIGHT,colors)
	print a
	print a.get_complete_area([0,0])

	a.set_start([0,0])
	print a
	print a.get_complete_area([0,0])

	embed()

	for i in range(10):
		print i
		a.set_color([0,0],(a[0,0]+1) % 5)
		print a
		print a.get_complete_area([0,0])

if __name__ == '__main__':
	main()