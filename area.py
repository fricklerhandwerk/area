# -*- coding: utf-8 -*-
import random,copy
from tabulate import tabulate

colors = ["red","green","blue","yellow","magenta"]

class Board():
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.area = [	[random.randint(0,len(colors)-1) for x in range(width)] \
		             							for x in range(height)]

		# set up starting corners
		self.set_start(0,0)
		self.set_start(self.height-1,self.width-1)

	def set_color_recursive(self,x,y,color):
		# set color to area around given cell
		ref = self.area[x][y]
		self.area[x][y] = color
		for a,b in self.get_neighbors(x,y):
			if self.area[a][b] == ref:
				self.set_color(a,b,color)

	def set_color(self,x,y,color):
		a,_ = self.get_area(x,y)
		for i,j in a:
			self.area[i][j] = color

	def get_neighbors(self,x,y):
		# return coordinates of neighbors
		dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
		return [	[x+a,y+b] for a,b in dirs if \
		        	all([x+a < self.height,y+b < self.width,x+a >= 0,y+b >= 0])]

	def get_area(self,x,y):
		# return coordinates of area of x,y and its border
		todo = [[x,y]]
		area = []
		border = []

		while todo != []:
			a,b = todo[0]
			area.append([a,b])

			border +=	filter( \
			         	lambda k: k not in border and \
			         	self.area[k[0]][k[1]] != self.area[x][y], \
			         	self.get_neighbors(a,b))

			todo +=	filter( \
			       	lambda k: k not in area and \
			       	self.area[k[0]][k[1]] == self.area[x][y], \
			       	self.get_neighbors(a,b))
			todo = todo[1:]

		return area,border

	def print_area(self,x,y):
		# print area of given cell as `*`, border as `X`, `:` else
		area = copy.deepcopy(self.area)
		a,b = self.get_area(x,y)
		for i in range(len(area)):
			for j in range(len(area[0])):
				if [i,j] in a:
					area[i][j] = '*'
				elif [i,j] in b:
					area[i][j] = 'X'
				else:
					area[i][j] = ':'
		print tabulate(area)

	def set_start(self,x,y):
		for a,b in self.get_neighbors(x,y):
			# set immediate neighbors to same color
			self.area[a][b] = self.area[x][y]
			for c,d in filter(lambda k: k != [x,y],self.get_neighbors(a,b)):
				# set 2nd-grade neighbors to different color
				if self.area[c][d] == self.area[x][y]:
					self.area[c][d] = (self.area[c][d] + 1) % (len(colors)-1)

	def __str__(self):
		return tabulate(self.area)

def main():
	HEIGHT = 5
	WIDTH = 10

	a = Board(WIDTH,HEIGHT)
	print a
	a.print_area(0,0)

	for i in range(10):
		print i
		a.set_color(0,0,(a.area[0][0]+1) % 5)
		print a
		a.print_area(0,0)


if __name__ == '__main__':
	main()