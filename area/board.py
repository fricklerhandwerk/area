# -*- coding: utf-8 -*-
import random,copy
from tabulate import tabulate

class Board():
    """
    Area board model with methods to read and manipulate board state
    """
    def __init__(self,height,width,colors):
        """
        create random board with given parameters
        """

        assert len(colors)  > 1, "colors list too short, length must be > 1"
        assert height       > 0, "height too small, must be > 0"
        assert width        > 0, "width too small, must be > 0"

        self.height = height
        self.width  = width
        self.colors = colors
        self.area   = [[random.randrange(len(colors)) for x in range(width)] \
                        for x in range(height)]

    def __getitem__(self,key):
        x,y = key
        return self.area[x][y]

    def __setitem__(self,key,value):
        x,y             = key
        self.area[x][y] = value

    def __str__(self):
        return tabulate(self.area)

    def set_start(self,x,color):
        """
        set a start point at `x`, return starting area

        makes sure that the neighbors of `x` have the same color
        while the surrounding cells are different
        """

        assert x[0] in xrange(self.height), "height coordinate out of bound"
        assert x[1] in xrange(self.width), "width coordinate out of bound"

        colors = len(self.colors)
        self[x] = color
        for i in self.get_neighbors(x):
            # set immediate neighbors to same color
            self[i] = color
            n = [k for k in self.get_neighbors(i) if k != x]
            for j in n:
                # set 2nd-grade neighbors to different color
                if self[j] == color:
                    self[j] = (self[j] + 1) % colors
        return self.get_area({x},self.get_neighbors(x),color)

    def get_neighbors(self,x):
        """
        return coordinates of neighbors of `x` as list
        """

        x,y = x

        assert x in xrange(self.height)
        assert y in xrange(self.width)

        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # only return those inside board
        return [(x+a,y+b) for a,b in dirs if \
            all([x+a < self.height,y+b < self.width,x+a >= 0,y+b >= 0])]

    def get_area(self,area,border,color):
        """
        grow a given `area` using its `border` such that
        neighboring cells having `color` are incorporated

        Args:
            area    set representing existing area
            border  set representing border of `a`
            color   color of neighbors to add
        Returns:
            area    new set representing larger area of same color that contains `a`
            border  new set representing border of `area`
        NOTE:
            to get area around single cell, call
                get_area({x},self.get_neighbors(x),self[x])
        """

        assert border != set(), "if border empty, area cannot be updated"

        # create local copies for return
        # NOTE: this is primarily about clarity. for better performance one can
        #       work on the original data at the risk of possible side effects
        #       by instead using the following.
        #
        # todo = border
        # border = []
        #
        todo = set(border)
        area = set(area)
        border = set()

        # breadth first search starting from border, avoiding old area
        while todo:
            x = todo.pop()

            if self[x] == color:
                area.add(x)

                neighbors = filter( lambda k:   k not in border and \
                                                k not in area,
                                    self.get_neighbors(x))

                border |= set(k for k in neighbors if self[k] != color)

                todo |= set(k for k in neighbors if self[k] == color)
            else:
                border.add(x)

        return area, border

    def get_enclosed_area(self,area,border,target):
        """
        return coordinates from which `target` cannot be reached without
        going through `area`

        Args:
            area    set representing an area
            border  list representing border of `area`
            target  set of coordinates to check reachability against
        Returns:
            components  set of coordinates enclosed by `area`
        """

        assert border != set(), "if border empty, neighboring regions cannot be computed"

        todo = border - target  # drop border cells if they belong to other players
        components = set()      # list of enclosed components found

        while todo:
            # check reachability of `target` by picking a border cell
            x = todo.pop()
            # start a new component
            todo2 = {x}
            component = set()
            enclosed = True
            # fill it with neighbors not in original area
            # until a cell from `target` is caught or `todo2` empty
            while todo2:
                y = todo2.pop()
                component.add(y)
                neighbors = set(filter( lambda k:   k not in area and \
                                                    k not in component, \
                                        self.get_neighbors(y)))

                todo2 |= neighbors
                # if `target` reached, component will be discarded
                if any(x in target for x in neighbors):
                    enclosed = False
                    break
            # consume the rest of discarded component's border cells
            # so we don't search it again next time
            while todo2:
                y = todo2.pop()
                component.add(y)
                todo2 |=    set(filter( lambda k:   k not in component and \
                                                    k in border, \
                                        self.get_neighbors(y)))
            if enclosed:
                components |= component
            # shrink search space for next iteration
            todo -= component
        return components

    def set_color(self,area,color):
        """
        set `area` to `color`
        """

        assert color in xrange(len(self.colors))

        for x,y in area:
            assert x in xrange(self.height)
            assert y in xrange(self.width)
            self[x,y] = color

    def get_complete_area(self,x):
        """
        return area of coordinate `x` as `True`, border as `False`, `None` else
        """

        assert x[0] in xrange(self.height)
        assert x[1] in xrange(self.width)

        area = copy.deepcopy(self)
        a,b = area.get_area({x},self.get_neighbors(x),self[x])
        for i in range(area.height):
            for j in range(area.width):
                if (i,j) in a:
                    area[i,j] = True
                elif (i,j) in b:
                    area[i,j] = False
                else:
                    area[i,j] = None
        return area

