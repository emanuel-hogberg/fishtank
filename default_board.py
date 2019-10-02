from board import *
import random

class BoardCreation():
    def CreateTiles(self, num):
        tiles = list()
        for i in range(num):
            tiles.append(Tile(i))
        
        tiles[0].edges[1] = tiles[1]
        for i in range(1, num - 1):
            tiles[i].edges[1] = tiles[i + 1]
            tiles[i].edges[4] = tiles[i - 1]
        tiles[-1].edges[4] = tiles[-2]
        return tiles

    # given a row of tiles, add one row below it with one additional tile added.
    def ExpandTiles(self, tiles):

        # Add the given tile to leftmost bottom position, then add a new tile to the rightmost bottom tile and continue recursively.
        def AddOneTile(tiles, first_left_tile, i=0):
            SW(tiles[0], first_left_tile)
            #tiles[0].edges[3] = first_left_tile
            right_tile = Tile("{}:r{}".format(tiles[0], i))
            SE(tiles[0], right_tile)
            #tiles[0].edges[2] = right_tile = Tile("{}{}{}".format(tiles[0], ':r', i))
            E(first_left_tile, right_tile)
            if len(tiles) == 1:
                return [right_tile]
            return [right_tile] + AddOneTile(tiles[1:], right_tile, i+1)

        (first_tile, second_tile) = (Tile('L0'), Tile('R0'))
        # tiles[0].edges[3] = first_tile
        # tiles[0].edges[2] = second_tile
        SW(tiles[0], first_tile)
        SE(tiles[0], second_tile)
        E(first_tile, second_tile)

        return [first_tile, second_tile] + AddOneTile(tiles[1:], second_tile)

    # given a row of tiles, add one row below it with one less tile
    def ReduceTiles(self, tiles):
        new_row = []
        for i in range(0, len(tiles) - 1):
            new_row += [Tile("{}n:{}".format(tiles[i], i))]
            if i > 0:
                E(new_row[i - 1], new_row[i])
            SE(tiles[i], new_row[i])
            SW(tiles[i+1], new_row[i])
        return new_row

class DefaultBoard(BoardCreation):

    # --012--
    # -34 56-
    # 78 9 ab
    # -cd ef-
    # --ghi--
    def create_board(self):
        tiles = [self.CreateTiles(3)]
        tiles += [self.ExpandTiles(tiles[0])]
        tiles += [self.ExpandTiles(tiles[1])]
        tiles += [self.ReduceTiles(tiles[2])]
        tiles += [self.ReduceTiles(tiles[3])]

        # rename all tiles
        new_names = list(range(0, 10)) + list("abcdefghi")
        for row in tiles:
            s = ""
            for n in row:
                n.name = str(new_names.pop(0))
                s += n.name + ", "
            print(s)

        tiles[2][2].type = Land.DESERT
        tiles[2][2].bandit = True

        # assign lands
        def repeat_land(land_tuple):
            def add_lands(t, n):
                if n <= 1:
                    return [t]
                tail = add_lands(t, n - 1)
                return [t] + tail
                # return [t] + add_lands(t, n - 1) if n > 1 else [t]
            return add_lands(land_tuple[0].value, land_tuple[1])

        lands_sorted = [(Land.WOOD, 4),
                (Land.SHEEP, 4),
                (Land.WHEAT, 4),
                (Land.STONE, 3),
                (Land.BRICK, 3)]
        lands = []
        for l in lands_sorted:
            lands += repeat_land(l)
        random.shuffle(lands)
        
        for tile_row in tiles:
            for n in tile_row:
                if n.type is Land.UNKNOWN:
                    n.type = Land(lands.pop())
        
        # board values example:
        #    10 2 9
        #  12 6 4 10
        # 9 11    3 8
        #   8 3  4 5
        #    5 6 11
        #
        # tile names for reference:
        # --012--
        # -34 56-
        # 78 9 ab
        # -cd ef-
        # --ghi--
        vals = list([10, 2, 9, 10, 8, 5, 11, 6, 5, 8, 9, 12, 6, 4, 3, 4, 3, 11])
        i = random.randint(0, len(vals))
        direction = 1
        n = tiles[0][0]
        while len(vals) > 0:
            n.value = vals.pop(i if len(vals) > i else 0)
            s1 = "   {}, {}".format(n.edges[5], n.edges[0])
            s2 = "{}, <{}>, {}".format(n.edges[4], n, n.edges[1])
            s3 = "   {}, {}".format(n.edges[3], n.edges[2])
            
            while n.edges[direction] is None:
                direction = direction + 1 if direction < 5 else 0
            
            if (n.edges[direction].value != -1):
                direction = direction + 1 if direction < 5 else 0
            n = n.edges[direction]


        return tiles
