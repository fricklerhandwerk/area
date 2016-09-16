# -*- coding: utf-8 -*-
import random, board

class Game():
	"""
	Area game model with all the rules
	"""
	def __init__(	self, height=28, width=40,\
	             	colors=["red","green","blue","yellow","magenta"],\
	             	color_enclosed=False, count_enclosed=True, win_enclosed=False):

		"""
		create game, assume 2 players hard coded
		"""

		# len(colors) > len(players) actually
		assert len(colors)	> 2, "colors list too short, length must be > 2"
		assert height     	> 4, "height too small, must be > 4"
		assert width      	> 4, "width too small, must be > 4"

		# set up board
		self.area = board.Board(height,width,colors)
		self.colors = range(len(colors)) # we only need the indices

		## handling of enclosed areas
		## NOTE: use exactly one for efficiency
		# color enclosed area immediately
		self.color_enclosed = color_enclosed
		# count enclosed area for score
		# NOTE: is implied by `color_enclosed`
		self.count_enclosed = count_enclosed
		# win condition based on enclosed area
		# NOTE: is implied by `count_enclosed`
		self.win_enclosed = win_enclosed

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
		set up players' start positions and colors
		"""

		# create players
		self.players = []
		height = self.area.height
		width = self.area.width
		# assign unique colors randomly
		c = random.sample(self.colors,len(self.colors))
		self.players.append(Player("Player 1",(0,0),c.pop()))
		self.players.append(Player("Player 2",(height-1,width-1),c.pop()))

		for p in self.players:
			# set up start position, assign player's area and color
			p.area,p.border = self.area.set_start(p.pos,p.color)
			self.update_player(p)

	def command(self,p,c):
		"""
		try to fulfill player command

		return `True` if game state changed, `False` otherwise
		"""

		assert p in xrange(len(self.players))
		assert c in self.colors

		# make sure it's player's turn and
		# chosen color is not used by other players
		if	p == self.turn and c in self.colors_available(p):
		  	p = self.players[p]
		  	# set new color to player's area
		  	self.color_player(p,c)
		  	# update player state
		  	self.update_player(p)
		  	# go to next turn
		  	self.next_turn()
		  	return True
		else:
			return False

	def colors_available(self,p):
		"""
		return set of colors available for a player
		"""
		if p == self.turn:
			return set(self.colors) - self.colors_used()
		else:
			return set()

	def colors_used(self):
		"""
		return set of colors used by players
		"""
		return set(x.color for x in self.players)

	def color_player(self,p,c):
		"""
		set new color to player's area
		"""

		self.area.set_color(p.area,c)
		if self.color_enclosed:
			# also color enclosed components
			a,b = self.area.get_area(p.area,p.border,c)
			comps = self.area.get_enclosed_area(a,b,self.get_other_areas(p))
			self.area.set_color(comps,c)

	def update_player(self,p):
		"""
		after change of game state, update player properties
		that depend on the game

		we do this here so that `Player` can stay a dumb data structure.
		otherwise it would need information about board and game.
		"""

		# update color
		p.color = self[p.pos]
		# update area/border/enclosed
		p.area,p.border = self.area.get_area(p.area,p.border,p.color)
		p.enclosed = self.area.get_enclosed_area(p.area,p.border,self.get_other_areas(p))
		# compute score from ratio of area and board
		a = len(p.area)
		b = a + len(p.enclosed) # area and enclosed area never intersect
		w = self.area.width
		h = self.area.height
		p.score = a/(h*w/2.0)
		p.escore = b/(h*w/2.0)
		if self.count_enclosed:
			p.score = p.escore

	def get_other_areas(self,p):
		"""
		get the area all other players occupy
		"""
		# get areas of other players
		others = (x.area for x in self.players if x != p)
		# flatten coordinates lists
		return set(i for a in others for i in a)

	def next_turn(self):
		self.turn = (self.turn + 1) % len(self.players)

	def winner(self):
		"""
		return winning player or None
		"""
		return next((p for p in self.players if self.wins(p)),None)

	def wins(self,p):
		"""
		decide if player `p` wins
		"""
		if self.win_enclosed:
			# based on enclosed area
			return p.escore >= 1
		else:
			# based on normal area
			return p.score >= 1

class Player():
	"""
	Area player model
	"""

	def __init__(self,name,pos,color):
		"""
		create player
		"""
		self.name = name
		self.pos = pos
		self.color = color
		self.score = 0
		self.escore = 0 # include enclosed area
		self.area = set([pos])
		self.border = set()
		self.enclosed = set()

	def __str__(self):
		return ' '.join(map(str,[self.name,self.pos,self.score]))

	def __repr__(self):
		return ','.join(map(repr,[self.name,self.pos,self.score]))
