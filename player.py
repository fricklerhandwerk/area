# -*- coding: utf-8 -*-

class Player():
	"""
	Area player model
	"""

	def __init__(self,name,pos):
		"""
		create player
		"""

		self.name = name
		self.pos = pos
		self.score = 0

	def __str__(self):
		return ' '.join(map(str,[self.name,self.pos,self.score]))

	def __repr__(self):
		return ','.join(map(repr,[self.name,self.pos,self.score]))
