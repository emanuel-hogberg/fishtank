from enum import Enum
import math

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
        self.harbour = None
    
    def neighbor(self, tile, direction):
        self.edges[direction.value] = tile
        tile.edges[direction.value - 3] = self

    def __str__(self):
        return ('{} {} ({})'.format(self.type, self.value, self.name)) if self.value > -1 else str(self.name)
    
    def description(self):
        return "{} [{}]".format(str(self), "".join(map(lambda neighbor: "-" if neighbor is None else str(neighbor.name), self.edges)))

# A corner is based on a tile and a direction, e.g. 0 = upper corner from given tile
class Corner:
    def __init__(self, tile, direction_int):
        self.tile = tile
        self.direction_int = direction_int

        # find which tiles surround this corner.
        # direction_int is where the corner is situated:
        #   ^0
        # 5< >1
        # 4< >2
        #   v3
        self.tiles = [tile, \
            tile.edges[direction_int - 1 if direction_int > 0 else 5], \
            tile.edges[direction_int]]
        self.tiles[0].corners[direction_int] = self
        if not self.tiles[1] is None:
            self.tiles[1].corners[direction_int + 2 if direction_int + 2 <= 5 else direction_int - 4]
        if not self.tiles[2] is None:
            self.tiles[2].corners[direction_int + 4 if direction_int + 4 <= 5 else direction_int - 2]
        self.position = None

    def init_corner_position(self, tile_width, tile_height):
        stile = self.tile.stile
        (tx, ty) = stile.rect.x, stile.rect.y
        half_width = tile_width / 2
        self.position = {
            0: (tx + half_width, ty),
            1: (tx + tile_width, ty),
            2: (tx + tile_width, ty + tile_height),
            3: (tx + half_width, ty + tile_height),
            4: (tx, ty + tile_height),
            5: (tx, ty)
        }.get(self.direction_int)
        
    def distance_to_point(self, x, y):
        return math.sqrt( (x - self.position[0]) ** 2 + (y - self.position[1]) ** 2)

class Harbour:
    def __init__(self, tile, edge_id, land_type):
        self.type = land_type # .ANY = the 1:3 trade
        self.tile = tile
        self.edge_id = edge_id
        self.bridges = (edge_id, edge_id + 1 if edge_id < 5 else 0)
        self.sprite = None

        tile.harbour = self

