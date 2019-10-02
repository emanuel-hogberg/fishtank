from enum import Enum

class Land(Enum):
    WOOD = 1
    BRICK = 2
    STONE = 3
    SHEEP = 4
    WHEAT = 5
    DESERT = 6
    GOLD = 7
    OCEAN = 8
    UNKNOWN = -1
    ANY = -2

class LandColor:
    def color(self, e):
        return {
            1: (0, 140, 0),
            2: (220, 40, 0),
            3: (100, 100, 100),
            4: (225, 225, 225),
            5: (245, 245, 0),
            6: (210, 200, 70),
            7: (0, 200, 0),
            8: (0, 0, 200),
            -1: (50, 0, 0),
            -2: (50, 50, 50)
        }.get(e if e is int else e.value)

class HexDirection(Enum):
    NE = 0
    E = 1
    SE = 2
    SW = 3
    W = 4
    NW = 5

def SW(upper_right, lower_left):
    upper_right.neighbor(lower_left, HexDirection.SW)
def SE(upper_left, lower_right):
    upper_left.neighbor(lower_right, HexDirection.SE)
def E(left, right):
    left.neighbor(right, HexDirection.E)

class Tile:
    def __init__(self, name):
        self.name = name

        # Edges clockwise (corner, edge, corner, edge ..., hexagonally with vertical sides)
        #  5/\0
        # 4|  |1
        #  3\/2
        self.edges = [None] * 6

        # Corners clockwise
        #   ^0
        # 5< >1
        # 4< >2
        #   v3
        self.corners = [None] * 6
        self.value = -1
        self.type = Land.UNKNOWN
        self.bandit = False
        self.pirate = False
        # stile is the strite tile from sprites.py
        self.stile = None
    
    def neighbor(self, tile, direction):
        self.edges[direction.value] = tile
        tile.edges[direction.value - 3] = self

    def __str__(self):
        return ('{} {} ({})'.format(self.type, self.value, self.name)) if self.value > -1 else str(self.name)
    
    def description(self):
        return "{} [{}]".format(str(self), "".join(map(lambda neighbor: "-" if neighbor is None else str(neighbor.name), self.edges)))

class Corner:
    def __init__(self, tile, direction_int):
        
        # find which tiles surround this corner.
        # direction_int is where the corner is situated:
        #   5__0
        # 4<    >1
        #   3__2

        self.tiles = [tile, \
            tile.edges[direction_int], \
            tile.edges[direction_int + 1 if direction_int < 5 else 0]]

class Harbour:
    def __init__(self):
        self.type = Land.UNKNOWN # .ANY = the 1:3 trade
