# -*- coding: utf-8 -*-
import random, board
from wx.lib.pubsub import pub

class Game():
	"""
	Area game model
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

		# create players
		# TODO: generalize to distribute arbitrary number of players evenly
		self.players = []
		self.players.append(Player("Player 1",(0,0)))
		self.players.append(Player("Player 2",(height-1,width-1)))

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
			# initialize color
			# WARNING: do not remove, very important!
			p.color = self[p.pos]

			# get other players' colors in use
			used = self.colors_used()
			used.remove(p.color)
			# set different color if already used
			if p.color in used:
				# get all that is left
				rest = [x for x in self.colors if x not in used]
				# set to one of unused colors
				self.area.set_color({p.pos},random.choice(rest))
			# set up start position, assign player's area and color
			p.area,p.border = self.area.set_start(p.pos)
		for p in self.players:
			self.update_player(p)

	def command(self,p,c):
		"""
		try to fulfill player command
		"""

		assert p in xrange(len(self.players))
		assert c in self.colors

		# make sure it's player's turn and
		# chosen color is not used by other players
		if	p == self.turn and c in self.colors_available(p):
		  	p = self.players[p]
		  	# set new color to player's area
		  	self.area.set_color(p.area,c)

			# color enclosed area
			if self.color_enclosed:
				self.set_color_enclosed(p,c)

			# update player state
			self.update_player(p)
			# go to next turn
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
			p = self.players[p]
			used = set(self.colors_used())
			# exclude colors not bordering
			_,border = self.area.get_area(p.area,p.border)
			bordering = set([self[x] for x in border])
			available = set(self.colors) & bordering - used
			if available:
				return available
			else:
				# if none left bordering, return all that are not used
				return set(self.colors) - used
		else:
			return []

	def next_turn(self):
		self.turn = (self.turn + 1) % len(self.players)

	def colors_used(self):
		"""
		return list of colors used by players
		"""
		# must be a list to deal with duplicates in `self.set_players()`
		return [x.color for x in self.players]

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
			# compute based on enclosed area
			a,_,_ = self.area.get_enclosed_area(p.area,p.border,self.get_other_areas(p))
			w = self.area.width
			h = self.area.height
			return len(a)/(h*w/2.0) >= 1
		else:
			# compute based on normal score
			return p.score >= 1

	def update_player(self,p):
		"""
		after change of game state, update player properties
		that depend on the game
		"""
		# we do this here so that `Player` can stay a dumb data structure
		# update color
		p.color = self[p.pos]
		# update area/border
		p.area,p.border = self.area.get_area(p.area,p.border)
		if self.count_enclosed:
			# compute score from ratio of *enclosed* area and board
			a,_,_ = self.area.get_enclosed_area(p.area,p.border,self.get_other_areas(p))
		else:
			# compute score from ratio of colored area and board
			a = p.area
		w = self.area.width
		h = self.area.height
		p.score = len(a)/(h*w/2.0)

	def set_color_enclosed(self,p,c):
		"""
		color enclosed components of player `p`'s area
		"""
		# update player's area before coloring
		pa,pb = self.area.get_area(p.area,p.border)
		# enclosed components
		p.area,p.border,comps = self.area.get_enclosed_area(pa,pb,self.get_other_areas(p))
		for comp in comps:
			self.area.set_color(comp,c)

	def get_other_areas(self,p):
		"""
		get the area all other players occupy
		"""
		# get areas of other players
		others = map(lambda x: x.area,filter(lambda x: x != p,self.players))
		# flatten coordinates lists
		others = [i for a in others for i in a]
		return set(others)


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
		self.color = None
		self.score = 0
		self.area = set()
		self.border = []

	def __str__(self):
		return ' '.join(map(str,[self.name,self.pos,self.score]))

	def __repr__(self):
		return ','.join(map(repr,[self.name,self.pos,self.score]))
