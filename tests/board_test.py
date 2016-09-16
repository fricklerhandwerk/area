# -*- coding: utf-8 -*-
from area import board

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

@given(	integers(min_value=-50, max_value=50),\
       	integers(min_value=-50, max_value=50),\
       	lists(integers(),max_size=20))
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
       	integers(min_value=10, max_value=50),\
       	integers(min_value=10, max_value=50),\
       	lists(integers(),min_size=2,max_size=10))
def test_set_start_color(p1,p2,x,y,l):
	"""
	immediate neighbors of starting cell have same color and
	the border around them has different colors
	"""

	p = (p1,p2)
	b = board.Board(x,y,l)
	try:
		c = b[p]
	except IndexError:
		assert True
	else:
		try:
			area,border = b.set_start(p,c)
		except AssertionError:
			assert True
		else:
			assert all(map(lambda x: b[x] == c,area))
			assert all(map(lambda x: b[x] != c,border))

@given(	integers(),integers(),\
       	integers(min_value=10, max_value=50),\
       	integers(min_value=10, max_value=50),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_neighbors_count(p1,p2,x,y,l):
	"""
	a cell has at most 4 neighbors
	"""

	p = (p1,p2)
	b = board.Board(x,y,l)
	try:
		n = b.get_neighbors(p)
	except AssertionError:
		assert True
	else:
		assert len(n) <= 4

@given(	integers(),integers(),\
       	integers(min_value=10, max_value=50),\
       	integers(min_value=10, max_value=50),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_area_count(p1,p2,x,y,l):
	"""
	area and border around cell is not larger than whole board
	"""

	p = (p1,p2)
	b = board.Board(x,y,l)
	try:
		c = b[p]
	except IndexError:
		assert True
	else:
		try:
			area, border = b.set_start(p,c)
		except AssertionError:
			assert True
		else:
			assert len(area) + len(border) <= x*y
			assert len(area) > 0

@given(	integers(),integers(),integers(),\
       	integers(min_value=10, max_value=50),\
       	integers(min_value=10, max_value=50),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_area_size(p1,p2,c,x,y,l):
	"""
	area/border display has same size as area/border coordinates
	"""

	p = (p1,p2)
	b = board.Board(x,y,l)

	try:
		area,border = b.set_start(p,c)
		comp = b.get_complete_area(p)
	except AssertionError:
		assert True
	else:
		c = filter(lambda x: x is True,concat(comp.area))
		assert len(c) == len(area)
		d = filter(lambda x: x is False,concat(comp.area))
		assert len(d) == len(border)


@given(	integers(),integers(),integers(),\
       	integers(min_value=10, max_value=50),\
       	integers(min_value=10, max_value=50),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_area_after_coloring(p1,p2,c,x,y,l):
	"""
	coloring an area results in area with at least same size
	"""

	p = (p1,p2)
	b = board.Board(x,y,l)
	try:
		area1,border1 = b.set_start(p,c)
		b.set_color(area1,c)
	except AssertionError:
		assert True
	else:
		area2,border2 = b.get_area(area1,border1,c)
		assert len(area2) >= len(area1)


@given(	integers(),integers(),\
       	integers(min_value=10, max_value=50),\
       	integers(min_value=10, max_value=50),\
       	lists(integers(),min_size=2,max_size=10))
def test_get_area_twice(p1,p2,x,y,l):
	"""
	getting an area twice results in same area
	"""

	p = (p1,p2)
	b = board.Board(x,y,l)
	try:
		c = b[p]
	except IndexError:
		assert True
	else:
		try:
			area1,border1 = b.set_start(p,c)
			area2,border2 = b.get_area(area1,border1,c)
		except AssertionError:
			assert True
		else:
			assert area1 == area2
			assert set(border1) == set(border2)

@given(	integers(),integers(),integers(min_value=0,max_value=9),\
       	integers(min_value=10, max_value=50),\
       	integers(min_value=10, max_value=50),\
       	lists(integers(),min_size=2,max_size=10))
def test_enclosed_area(p1,p2,c,x,y,l):
	"""
	enclosed area is larger or equal given area, border smaller equal than before,
	if components exist they are not empty
	"""

	p = (p1,p2)
	b = board.Board(x,y,l)
	try:
		area1,border1 = b.set_start(p,c)
		b.set_color(area1,c)
	except AssertionError:
		assert True
	else:
		area2,border2 = b.get_area(area1,border1,c)
		print b
		components = b.get_enclosed_area(area2,border2,{b[x-1,y-1]})
		area3 = area2 | components
		border3 = border2 - components
		assert len(area2) <= len(area3)
		assert len(border2) >= len(border3)
		if components:
			assert len(components) > 0
