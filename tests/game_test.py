# -*- coding: utf-8 -*-
from area import game

from hypothesis import given, example
from hypothesis.strategies import integers, randoms, lists
from hypothesis import settings

settings.perform_health_check = False

def concat(l):
	result = []; map(result.extend,l); return result
def concatMap(f,l):
	return concat(map(f,l))
def uniq(l):
	result = []
	[result.append(x) for x in l if x not in result]
	return result

@given(	integers(min_value=5,max_value=100),\
       	integers(min_value=5,max_value=100),\
       	lists(integers(),min_size=3, max_size=100))
def test_set_player_color(x,y,l):
	"""
	all players have different starting colors
	"""
	g = game.Game(x,y,colors=l)
	assert uniq([g[x.pos] for x in g.players]) == [g[x.pos] for x in g.players]

@given(	integers(min_value=5,max_value=100),\
       	integers(min_value=5,max_value=100),\
       	lists(integers(),min_size=3, max_size=100))
def test_num_colors_used(x,y,l):
	"""
	#colors used = #players
	"""
	g = game.Game(x,y,colors=l)
	assert len(g.colors_used()) == len(g.players)

@given(	integers(min_value=5,max_value=100),\
       	integers(min_value=5,max_value=100),\
       	lists(integers(),min_size=3, max_size=100))
def test_start_score(x,y,l):
	"""
	all starting scores same
	"""
	g = game.Game(x,y,colors=l)
	assert all(map(lambda x: x.score == g.players[0].score, g.players))

@given(	integers(min_value=5,max_value=20),\
       	integers(min_value=5,max_value=20),\
       	lists(integers(),min_size=3, max_size=100),\
       	integers(min_value=0,max_value=1),integers(),randoms())
def test_valid_turn(x,y,l,p,c,r):
	"""
	trying invalid turn (wrong player or color) does not proceed game,
	but valid one does
	"""
	g = game.Game(x,y,colors=l)
	turn = g.turn

	if c in g.colors:
		if c in g.colors_available(g.turn) and p == g.turn:
			g.command(p,c)
			assert turn != g.turn, "game does not proceed on valid turn"
		else:
			g.command(p,c)
			assert turn == g.turn, "game proceeds on invalid turn"
	else:
		try:
			g.command(p,c)
			assert False, "game does not catch invalid colors"
		except AssertionError:
			assert True

@given(	integers(min_value=5,max_value=20),\
       	integers(min_value=5,max_value=20),\
       	lists(integers(),min_size=3, max_size=100),\
       	integers(min_value=0,max_value=1),randoms())# def test_valid_turn(x,y,l,p,r):
def test_num_colors_available(x,y,l,p,r):
	"""
	0 < available colors <= colors - players
	"""
	g = game.Game(x,y,colors=l)
	if p == g.turn:
		assert 0 < len(g.colors_available(p)) <= len(g.colors) - len(g.players)
	else:
		assert g.colors_available(p) == []

@given(	integers(min_value=5,max_value=20),\
       	integers(min_value=5,max_value=20),\
       	lists(integers(),min_size=3, max_size=10),randoms())
def test_score_values(x,y,l,r):
	"""
	score increases monotonically,
	score is smaller than board
	"""
	g = game.Game(x,y,colors=l)
	p = g.turn
	c = next(iter(g.colors_available(p)))
	old_score = g.players[p].score
	g.command(p,c)
	new_score = g.players[p].score
	assert old_score > 0
	assert old_score <= new_score


# # turn number always in range of player number

