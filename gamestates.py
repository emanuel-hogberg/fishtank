import sprites

class GameState:
    def __init__(self, board_stiles, gameview):
        self.stiles = board_stiles
        self.tiles = list(map(lambda s: s.tile, self.stiles))
        self.gameview = gameview

class PlaceTownState(GameState):
    def __init__(self, board_stiles, gameview):
        super().__init__(board_stiles, gameview)
        
        self.pointer = sprites.SPointer()
        self.status_text = sprites.Text('*status*', 'Comic Sans MS', 30)
        (self.status_text.x, self.status_text.y) = (230, 3)

        gameview.all_sprites_list.add(self.pointer)
        gameview.sprites_foreground.add(self.pointer)
        gameview.all_texts.append(self.status_text)

    def update(self):
        stiles_hovering = [s for s in self.stiles if s.hover]
        if len(stiles_hovering) > 0:
            stile = stiles_hovering[0]
            self.pointer.hide = False

            # set pointer location to the closest available corner
            distances = map(lambda corner: (corner.distance_to_point(self.gameview.mouse_x, self.gameview.mouse_y), corner), \
                filter(lambda corner: corner, stile.tile.corners))
            distances = sorted(distances, key=lambda p: p[0])
            if len(distances) > 0:
                closest_corner = distances[0][1]
                self.pointer.set_position(closest_corner.position)
                self.status_text.update_text("{} [] {}, {} corners".format(
                    stile.tile.name, stile.tile.value,
                    sum(map(lambda c: 0 if c is None else 1, stile.tile.corners))))
        else:
            self.pointer.hide = True
            # self.status_text.update_text('-')


