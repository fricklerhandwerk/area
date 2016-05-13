# -*- coding: utf-8 -*-
import random, board
from wx.lib.pubsub import pub

class Game():
	"""
	Area game model
	"""
	def __init__(	self, height=28, width=40,\
	             	colors=["red","green","blue","yellow","magenta"]):

		"""
		create game, assume 2 players hard coded
		"""
		# TODO: generalize to arbitrary number of players

		# len(colors) > len(players) actually
		assert len(colors)	> 2, "colors list too short, length must be > 2"
		assert height     	> 4, "height too small, must be > 4"
		assert width      	> 4, "width too small, must be > 4"

		# set up board
		self.area = board.Board(height,width,colors)
		self.colors = range(len(colors)) # we only need the indices

		# create players
		# TODO: generalize to distribute arbitrary number of players evenly
		self.players = []
		self.players.append(Player("Player 1",[0,0],self))
		self.players.append(Player("Player 2",[height-1,width-1],self))

		# set up players
		self.set_players()

		# one of the players starts at random
		self.turn = random.randrange(len(self.players))

	def __getitem__(self,key):
		return self.area[key]

	def __setitem__(self,key,value):
		self.area[key]	= value

	def __str__(self):
		p = map(str,self.players)
		# mark active player
		for i in range(len(self.players)):
			if self.turn == i:
				p[i] += ' *'

		return '\n'.join([str(self.area)] + p)

	def set_players(self):
		"""
		set up players' start positions
		"""

		assert len(self.players) < len(self.colors), "not enough colors available"

		for p in self.players:
			# get other players' colors in use
			used = self.colors_used()
			used.remove(p.color)
			# set different color if already used
			if p.color in used:
				# get all that is left
				rest = [x for x in self.colors if x not in used]
				# set to one of unused colors
				self.area.set_color(p.pos,random.choice(rest))
			# set up start position
			self.area.set_start(p.pos)

	def command(self,p,c):
		"""
		try to fulfill player command
		"""

		assert p in xrange(len(self.players))
		assert c in self.colors

		# make sure it's player's turn and
		# chosen color is not used by other players
		if	p == self.turn and \
		  	c in self.colors_available(p):
		  	p = self.players[p]
		  	# set new color
		  	self.area.set_color(p.pos,c)
		  	# go to next turn
		  	p.update_score()
		  	self.next_turn()
		  	# check if game continues or ends
		  	if self.winner():
		  		pub.sendMessage("winner",winner=self.winner())
		  	else:
		  		pub.sendMessage("next turn")

	def colors_available(self,p):
		"""
		return list of colors available for a player, removes non-bordering as well
		"""
		if p == self.turn:
			used = set(self.colors_used())
			# exclude colors not bordering
			border = self.area.get_border(self.players[p].pos)
			bordering = set([self[x] for x in border])
			available = list(set(self.colors) & bordering - used)
			if available:
				return available
			else:
				# if none left, return all that are not used
				return list(set(self.colors) - used)
		else:
			return []

	def next_turn(self):
		self.turn = (self.turn + 1) % len(self.players)

	def colors_used(self):
		"""
		return list of colors used by players
		"""
		# must be a list to deal with duplicates
		return [x.color for x in self.players]

	def winner(self):
		"""
		return winning player or None
		"""
		return next((p for p in self.players if p.score_relative >= 1),None)

class Player():
	"""
	Area player model
	"""

	def __init__(self,name,pos,game):
		"""
		create player
		"""

		self.name = name
		self.pos = pos
		self.game = game	# game player belongs to
		self.score = 0
		self.area = []

	@property
	def color(self):
		"""
		get player's color in given game
		"""
		return self.game[self.pos]

	@property
	def score_relative(self):
		"""
		get score relative to half the board size
		"""
		w = self.game.area.width
		h = self.game.area.height
		a = self.score
		return a/(w*h/2.0)

	def update_score(self):
		# TODO: compute score based on *enclosed* area
		self.score = len(self.game.area.get_area(self.pos))

	def update_area(self):
		self.area = self.game.area.get_extended_area(self.area)

	def __str__(self):
		return ' '.join(map(str,[self.name,self.pos,self.score]))

	def __repr__(self):
		return ','.join(map(repr,[self.name,self.pos,self.score]))

