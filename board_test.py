# -*- coding: utf-8 -*-
import board

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

@given(	integers(min_value=-100, max_value=100),\
       	integers(min_value=-100, max_value=100),\
       	lists(integers(),max_size=100))
def test_board_creation(x,y,l):
	"""
	board is always created with
	width > 1
	height > 1
	colors > 2
	"""

	try:
		a = board.Board(x,y,l)
	except AssertionError:
		assert True
	else:
		assert a.height > 0
		assert a.width > 0
		assert len(a.colors) > 1

@given(	integers(),integers(),\
       	integers(min_value=2, max_value=100),\
       	integers(min_value=2, max_value=100),\
       	lists(integers(),min_size=2,max_size=10))
def test_set_start_color(p1,p2,x,y,l):
	"""
	immediate neighbors of starting cell have same color and
	the border around them has different colors
	"""

	p = [p1,p2]
	a = board.Board(x,y,l)
	try:
		a.set_start(p)
	except AssertionError:
		assert True
	else:
		n = a.get_neighbors(p)
		assert all(map(lambda x: a[x] == a[p],n))
		nn = uniq(filter(lambda x: x != p,concatMap(a.get_neighbors,n)))
		assert all(map(lambda x: a[x] != a[p],nn))

@given(	integers(),integers(),\
       	integers(min_value=1, max_value=100),\
       	integers(min_value=1, max_value=100),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_neighbors_count(p1,p2,x,y,l):
	"""
	a cell has at most 4 neighbors
	"""

	p = [p1,p2]
	a = board.Board(x,y,l)
	try:
		n = a.get_neighbors(p)
	except AssertionError:
		assert True
	else:
		assert len(n) <= 4

@given(	integers(),integers(),\
       	integers(min_value=2, max_value=100),\
       	integers(min_value=2, max_value=100),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_area_count(p1,p2,x,y,l):
	"""
	area around cell is not larger than whole board
	"""

	p = [p1,p2]
	a = board.Board(x,y,l)
	try:
		a.set_start(p)
		j,k = a.get_area(p)
	except AssertionError:
		assert True
	else:
		assert len(j) <= x*y
		assert len(j) > 0

@given(	integers(),integers(),integers(),\
       	integers(min_value=2, max_value=100),\
       	integers(min_value=2, max_value=100),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_area_size(p1,p2,c,x,y,l):
	"""
	area/border display has same size as area/border coordinates
	"""

	p = [p1,p2]
	test = board.Board(x,y,l)

	try:
		a,b = test.get_area(p)
		comp = test.get_complete_area(p)
	except AssertionError:
		assert True
	else:
		c = filter(lambda x: x is True,concat(comp.area))
		assert len(c) == len(a)
		d = filter(lambda x: x is False,concat(comp.area))
		assert len(d) == len(b)


@given(	integers(),integers(),integers(),\
       	integers(min_value=2, max_value=100),\
       	integers(min_value=2, max_value=100),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_area_size(p1,p2,c,x,y,l):
	"""
	coloring an area results in area with at least same size
	"""

	p = [p1,p2]
	a = board.Board(x,y,l)
	try:
		r1,_ = a.get_area(p)

		a.set_color(p,c)
	except AssertionError:
		assert True
	else:
		r2,_ = a.get_area(p)
		assert len(r2) >= len(r1)
