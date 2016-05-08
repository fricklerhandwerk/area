# -*- coding: utf-8 -*-
import random,copy
from tabulate import tabulate

class Board():
	def __init__(self,width,height,colors):
		self.width 	= width
		self.height	= height
		self.colors	= colors
		# create random board
		self.area	= [[random.randint(0,len(self.colors)-1) for x in range(width)] \
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
		# set a starting point at x
		for i in self.get_neighbors(x):
			# set immediate neighbors to same color
			self[i] = self[x]
			for j in filter(lambda k: k != x,self.get_neighbors(i)):
				# set 2nd-grade neighbors to different color
				if self[j] == self[x]:
					self[j] = (self[j] + 1) % (len(self.colors)-1)

	def get_neighbors(self,x):
		# return coordinates of neighbors
		x,y = x
		dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
		return [	[x+a,y+b] for a,b in dirs if \
		        	all([x+a < self.height,y+b < self.width,x+a >= 0,y+b >= 0])]

	def get_area(self,x):
		# return coordinates of area of x and its border
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

			todo +=	filter( \
			       	lambda k: k not in area and \
			       	self[k] == self[x], \
			       	self.get_neighbors(y))
			todo = todo[1:]

		return area,border

	def set_color(self,x,color):
		a,_ = self.get_area(x)
		for i in a:
			self[i] = color

	# DEPRECATED

	def print_area(self,x):
		# print area of given cell as `*`, border as `X`, `:` else
		area = copy.deepcopy(self.area)
		a,b = self.get_area(x)
		for i in range(len(area)):
			for j in range(len(area[0])):
				if [i,j] in a:
					area[i][j] = '*'
				elif [i,j] in b:
					area[i][j] = 'X'
				else:
					area[i][j] = ':'
		print tabulate(area)

	def set_color_recursive(self,x,color):
		# set color to area around given cell
		ref    	= self[x]
		self[x]	= color
		for i in self.get_neighbors(x):
			if self[i] == ref:
				self.set_color_recursive(i,color)

def main():
	# just for testing

	HEIGHT = 5
	WIDTH = 10
	colors = ["red","green","blue","yellow","magenta"]

	a = Board(WIDTH,HEIGHT,colors)
	print a
	a.print_area([0,0])

	a.set_start([0,0])
	print a
	a.print_area([0,0])

	for i in range(10):
		print i
		a.set_color([0,0],(a[0,0]+1) % 5)
		print a
		a.print_area([0,0])

if __name__ == '__main__':
	main()