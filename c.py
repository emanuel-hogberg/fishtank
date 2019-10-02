from board import *
import pandas
import numpy
from functools import reduce
import sprites as sp
import random
import default_board
import gamestates

# Construct board
tiles = default_board.DefaultBoard().create_board()

print(reduce(lambda a, t: "{}, {}".format(a, str(len(t))), tiles, ""))

ll, tiles = tiles, []
for l in ll:
    tiles += l

print(", ".join(map(lambda tile: str(tile), tiles)))
# checking neighbors
print(", ".join(map(lambda tile: tile.description(), tiles[-2:])))

# test sprites
game = sp.GameView(gamestates.TestState())

tile_sprites = [sp.STile(t) for t in tiles] # list(map(lambda t: sp.STile(t), tiles))
for sprite in tile_sprites:
    game.all_sprites_list.add(sprite)

# set tile positions
def set_desert_pos(t):
    t.set_position(300, 200)
    t.tile.name += " DESERT"

[set_desert_pos(t) for t in tile_sprites if t.tile.type == Land.DESERT]

def set_remaining_positions(tile_sprites):
    return [t for t in tile_sprites if not t.set_position_from_neighbors()]
    # not_yet = []
    # for t in tile_sprites:
    #     if not t.set_position_from_neighbors():
    #         not_yet += t
    # return not_yet

not_yet = [] # tile_sprites
while len(not_yet) > 0:
    print("{} positions remaining...".format(len(not_yet)))
    not_yet = set_remaining_positions(not_yet)

# manually set positions of default board
(x, y) = (leftest, top) = (160, 80)
margin = 2
(x_step, y_step, adj_step) = (game.defs.e + margin, game.defs.e + margin, (game.defs.e + margin) / 2)
passed = 0
for col in range(5):
    (cs, x_adj) = (3, 0)
    if col == 1 or col == 3:
        (cs, x_adj) = (4, -adj_step)
    if col == 2:
        (cs, x_adj) = (5, -adj_step * 2)
    x += x_adj

    for row in range(cs):
        i = passed + row
        tile_sprites[i].set_position(x, y)
        x += x_step
    passed += cs
    y += y_step
    x = leftest

print("found all positions!")
for n in tile_sprites:
    if n.tile.value != 7:
        game.all_texts.append(sp.DieText(n))
    print("{} value: {}".format(n.tile.name, n.tile.value))
# s.draw()

game.all_texts.append(sp.MouseText('hej', 'Comic Sans MS', 30))

run = True
while run:
    game.run()
    run = game.exit_message == "RESTART"