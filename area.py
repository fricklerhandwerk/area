# -*- coding: utf-8 -*-
import random
from tabulate import tabulate

WIDTH = 10
HEIGHT = 5

colors = ["red","green","blue","yellow","magenta"]

def sign(x): return 1 if x >= 0 else -1

def neg(x): return -1 if x < 0 else 0

class Board():
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.area = [	[random.randint(0,len(colors)-1) for x in range(width)] \
		             	for x in range(height)]

		# set up starting corners
		self.set_corners()
		self.set_edge()

	def set_color(self,x,y,color):
		ref = self.area[x][y]
		self.area[x][y] = color
		for a,b in self.neighbors(x,y):
			if self.area[a][b] == ref:
				self.set_color(a,b,color)


	def neighbors(self,x,y):
		# return coordinates of neighbors
		dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
		return [	[x+a,y+b] for a,b in dirs if \
		        	all([x+a < self.height,y+b < self.width,x+a >= 0,y+b >= 0])]

	def set_corners(self):
		# set neighbors of starting point to same color
		for x,y in self.diagonal(1):
			self.area[x][y] = self.area[0][0]
			self.area[-x-1][-y-1] = self.area[-1][-1]

	def set_edge(self):
		# set neighbors of starting corner to different colors
		for x,y in self.diagonal(2):
			if self.area[x][y] == self.area[0][0]:
				self.area[x][y] = (self.area[x][y] + 1) % (len(colors)-1)
			if self.area[-x-1][-y-1] == self.area[-1][-1]:
				self.area[-x-1][-y-1] = (self.area[-x-1][-y-1] + 1) % (len(colors)-1)

	def diagonal(self,n):
		# return coordinates of n-th diagonal
		return [	[i+neg(n),n-i+neg(n)] \
		        	for i in range(0,n+sign(n),sign(n)) \
		        	if i+neg(n) < self.height and n-i+neg(n) < self.width]

	def __str__(self):
		return tabulate(self.area)

def main():

	a = Board(WIDTH,HEIGHT)
	a.set_color(0,0,a.area[0][0]+1 % 4)
	a.set_color(0,0,a.area[0][0]+1 % 4)
	a.set_color(0,0,a.area[0][0]+1 % 4)

	print a

if __name__ == '__main__':
	main()