import pygame as game
from board import LandColor

class CatanGraphicsDefaults:

    screen_width = 900
    screen_height = 800

    r = 80.0 # main scaler
    e = 1.0 * r

    vert_spacing = 30
    hor_spacing = 30

    die_text_pos_x = 0.2
    die_text_pos_y = 0.2
    pointer_size = 0.1 * e

    town_width = 0.23 * e
    town_height = 0.23 * e
    town_x_offset = town_width / 2
    town_y_offset = town_height / 2

    city_width = 0.3 * e
    city_height = 0.3 * e
    city_x_offset = town_width / 2
    city_y_offset = town_height / 2

    harbour_length_horizontal = e * 0.9 * 0.5
    harbour_length_vertical = e * 0.9
    harbour_x_offset = (e * 0.5 - harbour_length_horizontal) / 2
    harbour_y_offset = (e - harbour_length_vertical) / 2
    harbour_width = e * 0.04
    harbour_board_offset = e * 0.03

    def __init__(self):
        self.land_colors = LandColor()

class ZLayer:
    def __init__(self, name, z):
        self.name = name
        self.z = z

class CatanSprites(game.sprite.Sprite):

    def __init__(self):
        super().__init__()
        WHITE = (255, 255, 255)
        self.defs = CatanGraphicsDefaults()
        self.update_size(self.defs.e, self.defs.e)
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.color = (255, 0, 0)
        self.clicked = False
        self.hover = False
        self.image = game.Surface([self.defs.e, self.defs.e])
        self.image.fill((0, 0, 0))
        self.z_layer = None

    def update_size(self, width, height):
        self.image = game.Surface([width, height])
        self.width = width
        self.height = height
    
    def draw(self):
        if not self.removed:
            game.draw.ellipse(self.image, self.color, [0, 0, self.width, self.height])

    def set_position(self, x, y):
        (self.rect.x, self.rect.y) = (x, y)

class STile(CatanSprites):
    def __init__(self, tile):
        super().__init__()

        self.tile = tile
        tile.stile = self
        self.image = game.Surface([self.defs.e, self.defs.e])
        self.image.fill(self.defs.land_colors.color(tile.type))
        self.edge_positions = [None] * 6
    
    def has_position(self):
        return not (self.rect.x == self.rect.y == 0)

    # find the position of one of the neighbors and calculate this tile's position from that
    # - not used, not really working!
    def set_position_from_neighbors(self):
        if self.has_position():
            self.InitEdgePositions()
            return True
        
        vert_spacing = CatanGraphicsDefaults.vert_spacing
        hor_spacing = CatanGraphicsDefaults.hor_spacing

        found = False
        for i in range(0, len(self.tile.edges)):
            n = self.tile.edges[i]
            if n is None:
                continue
            if n.stile.has_position():
                (dx, dy) = {
                    0: (vert_spacing, -hor_spacing),
                    1: (0, -hor_spacing),
                    2: (-vert_spacing, -hor_spacing),
                    3: (vert_spacing, hor_spacing),
                    4: (0, -hor_spacing),
                    5: (vert_spacing, hor_spacing)
                }.get(i)
                self.set_position(n.stile.rect.x + dx, n.stile.rect.y + dy)
                found = True
                break
        if found:
            self.InitEdgePositions()
        return found
    
    def InitEdgePositions(self):
        half_width = self.width / 2
        quarter_width = self.width / 4
        half_height = self.height / 2
        
        if not self.edge_positions[5] is None:
            return
        
        self.edge_positions[5] = (self.rect.x + quarter_width, self.rect.y)
        self.edge_positions[0] = (self.rect.x + half_width + quarter_width, self.rect.y)
        self.edge_positions[1] = (self.rect.x + self.width, self.rect.y + half_height)
        self.edge_positions[2] = (self.rect.x + self.width - quarter_width, self.rect.y + self.height)
        self.edge_positions[3] = (self.rect.x + half_width - quarter_width, self.rect.y + self.height)
        self.edge_positions[4] = (self.rect.x, self.rect.y + half_height)
    
    def DistanceToEdge(self, x, y, edge_index):
        return 

class SPointer(CatanSprites):
    def __init__(self):
        super().__init__()
        
        self.hide = True
        self.color = (0, 0, 255)
    
        self.image = game.Surface([self.defs.pointer_size, self.defs.pointer_size])
        self.image.fill(self.color)

    def draw(self):
        if not self.hide:
            super().draw()
    
    def set_position(self, position):
        (self.rect.x, self.rect.y) = (position[0], position[1])

class SCorner(CatanSprites):
    
    def InitColorAndSize(self, color, width, height):
        self.image = game.Surface([width, height])
        self.image.fill(color)

class STown(SCorner):
    
    def __init__(self, player_color, corner):
        super().__init__()
        self.InitColorAndSize(player_color, self.defs.town_width, self.defs.town_height)

        self.player_color = player_color
        self.corner = corner
        corner.town = self
        self.set_position(corner.position[0] - self.defs.town_x_offset, corner.position[1] - self.defs.town_y_offset)
        self.is_city = False

    def UpgradeToCity(self):
        self.InitColorAndSize(self.player_color, self.defs.city_width, self.defs.city_height)
        self.set_position(self.corner.position[0] - self.defs.city_x_offset, self.corner.position[1] - self.defs.city_y_offset)

class SWithinTile(CatanSprites):
    
    def __init__(self, color):
        super().__init__()
        
        self.image = game.Surface([self.defs.e, self.defs.e])
        self.image.fill(color)

class SBandit(SWithinTile):
    
    def __init__(self, tile):
        super().__init__((0, 0, 0))

class SEdge(CatanSprites):

    def __init__(self, length_horizontal, length_vertical, width, edge_id, color, \
            tile, board_offset, board_x_offset, board_y_offset):
        super().__init__()
        
        self.image = game.Surface([self.defs.e, self.defs.e])
        self.image.fill(self.color)

        length = length_horizontal
        width = width
        horizontal = True
        if edge_id == 1 or edge_id == 4:
            horizontal = False
            length = length_vertical
        self.image = game.Surface([length if horizontal else width, width if horizontal else length])
        self.image.fill(color)
        self.color = color

        # set location based on tile position and corner
        corner = edge_id
        if corner == 2 or corner == 3 or corner == 4:
            corner += 1
        pos = tile.corners[corner].position
        x_offset = 0
        y_offset = 0
        
        if edge_id == 1 and tile.edges[1] is None:
            x_offset += board_offset
        if edge_id == 4 and tile.edges[4] is None:
            x_offset -= board_offset + width
        if edge_id == 0 and tile.edges[0] is None or edge_id == 5 and tile.edges[5] is None:
            y_offset -= board_offset + width
        if edge_id == 2 and tile.edges[2] is None or edge_id == 3 and tile.edges[3] is None:
            y_offset += board_offset
        if horizontal:
            x_offset += board_x_offset
        else:
            y_offset += board_y_offset
        self.set_position(pos[0] + x_offset, pos[1] + y_offset)

class SRoad(SEdge):

    def __init__(self, tile, player_color, edge_id):
        defs = CatanGraphicsDefaults()
        super().__init__(defs.harbour_length_horizontal, defs.harbour_length_vertical, \
            defs.harbour_width, edge_id, player_color, \
                tile, defs.harbour_board_offset, defs.harbour_x_offset, defs.harbour_y_offset)
        
        # self.image = game.Surface([self.defs.e, self.defs.e * 0.2])
        tile.roads[edge_id] = self

class SHarbour(SEdge):
    
    def __init__(self, harbour):
        defs = CatanGraphicsDefaults()
        super().__init__(defs.harbour_length_horizontal, defs.harbour_length_vertical, \
            defs.harbour_width, harbour.edge_id, defs.land_colors.color(harbour.type), \
                harbour.tile, defs.harbour_board_offset, defs.harbour_x_offset, defs.harbour_y_offset)

        self.harbour = harbour
class Text:
    def __init__(self, text, font_name, size):
        self.defs = CatanGraphicsDefaults()
        self.font = None
        self.surface = None
        self.font_name = font_name
        self.font_size = size
        self.text = text
        self.color = (0, 0, 0)
        self.x = 0
        self.y = 0
        self.removed = False
    
    def update_text(self, text):
        self.text = text

        if self.font is None:
            self.font = game.font.SysFont(self.font_name, self.font_size)
            self.surface = self.font.render(str(self.text), False, self.color)
        self.surface = self.font.render(str(text), False, self.color)

    def update(self, gameview):
        self.update_text(self.text)

    def draw(self, screen):
        if not self.removed:
            screen.blit(self.surface, (self.x, self.y))

# text that prints mouse position.
class MouseText(Text):
    def __init__(self, text, font_name, size):
        super().__init__(text, font_name, size)
        (self.x, self.y, self.font_size) = (800, 750, 10)

    def update(self, gameview):
        self.update_text("{},{}".format(gameview.mouse_x, gameview.mouse_y))

class DieText(Text):
    def __init__(self, stile):
        super().__init__(stile.tile.value, 'Comic Sans MS', 16)
        if stile.tile.value == 6 or stile.tile.value == 8:
            self.color = (255, 0, 0)
        (self.x, self.y) = (stile.rect.x + self.defs.e * self.defs.die_text_pos_x, stile.rect.y + self.defs.e * self.defs.die_text_pos_y)

class KeyState:
    def __init__(self):
        self.keys = None

    def update(self, gameview):
        self.keys = game.key.get_pressed()

# Restart game if R is pressed
class KeyRestartEvent(KeyState):
    def update(self, gameview):
        super().update(gameview)
        if self.keys[game.K_BACKSPACE]:
            gameview.exit_message = "RESTART"
            # trigger a QUIT event
            game.event.post(game.event.Event(game.QUIT))

# Quit game if Q is pressed
class KeyQuitEvent(KeyState):
    def update(self, gameview):
        super().update(gameview)
        if self.keys[game.K_q]:
            gameview.exit_message = "QUIT"
            # trigger a QUIT event
            game.event.post(game.event.Event(game.QUIT))

class KeyCancelActionEvent(KeyState):
    def __init__(self):
        super().__init__()

        self.cancel = False

    def update(self, gameview):
        super().update(gameview)
        self.cancel = self.keys[game.K_ESCAPE]

class KeyMainPhaseEvents(KeyState):
    def __init__(self):
        super().__init__()
        self.knight = False
        self.roll = False
        self.next_player = False
        self.build_road = False
        self.build_town = False
        self.build_city = False
        self.buy_development_card = False
    
    def update(self, gameview):
        super().update(gameview)
        self.knight = self.keys[game.K_k]
        self.roll = self.keys[game.K_SPACE]
        self.next_player = self.keys[game.K_n]
        self.build_road = self.keys[game.K_r]
        self.build_town = self.keys[game.K_t]
        self.build_city = self.keys[game.K_c]
        self.buy_development_card = self.keys[game.K_d]

class GameView:
    def __init__(self, starting_state):
        self.defs = CatanGraphicsDefaults()
        # used for drawing the sprites.
        self.all_sprites = game.sprite.Group()
        # self.sprites_foreground = game.sprite.Group()
        # self.sprites_background = game.sprite.Group()
        self.mouse_pos = None
        self.mouse_x = None
        self.mouse_y = None
        self.mouse_clicked = False
        self.clicked_sprites = []
        self.main_phase_key_events = KeyMainPhaseEvents()
        self.all_texts = []
        self.keys = []
        self.exit_message = ""
        self.game_state = starting_state
        self.z_layers = [
            ZLayer("Board", 0),
            ZLayer("Constructs", 1),
            ZLayer("Front", 2)
        ]
        self.z_layer_groups = dict(map(lambda z: (z, game.sprite.Group()), self.z_layers))
    
    def AddSprite(self, sprite, z_layer):
        self.all_sprites.add(sprite)
        if isinstance(z_layer, int):
            sprite.z_layer = list(filter(lambda z: z.z == z_layer, self.z_layers))[0]
        elif isinstance(z_layer, str):
            sprite.z_layer = list(filter(lambda z: z.name == z_layer, self.z_layers))[0]
        elif isinstance(z_layer, ZLayer):
            sprite.z_layer = z_layer
        else:
            raise Exception("Oh no you need to provide a z_layer from the gameView.z_layer list! or str or int.")
        self.z_layer_groups[sprite.z_layer].add(sprite)

    def RemoveSprite(self, sprite, z_layer):
        self.all_sprites.remove(sprite)
        self.z_layer_groups[sprite.z_layer].remove(sprite)
        
    def run(self):
        game.init()
        screen = game.display.set_mode([self.defs.screen_width, self.defs.screen_height])
        game.font.init()

        if any(filter(lambda sprite: sprite.z_layer is None, self.all_sprites)):
            raise Exception("z_layer {} has not been added through gameView.AddSprite()!")
        
        self.keys = [KeyRestartEvent(), KeyQuitEvent(), self.main_phase_key_events]

        # Loop until the user clicks the close button.
        done = False
        
        # Used to manage how fast the screen updates
        clock = game.time.Clock()
        
        # -------- Main Program Loop -----------
        while not done:
            events = game.event.get()
            for event in events:
                if event.type == game.QUIT:
                    done = True
        
            # Clear the screen
            screen.fill((255,255,255))

            # save mouse state
            self.mouse_pos = game.mouse.get_pos()
            self.mouse_x = self.mouse_pos[0]
            self.mouse_y = self.mouse_pos[1]
            
            self.clicked_sprites = filter(lambda e: e.type == game.MOUSEBUTTONUP, events)
            self.mouse_clicked = any(self.clicked_sprites)

            # update keys
            [k.update(self) for k in self.keys]
            
            # set all sprite clicked states
            for s in [s for s in self.all_sprites]:
                s.clicked = False
                s.hover = False
            for s in [s for s in self.all_sprites if s.rect.collidepoint(self.mouse_pos)]:
                s.clicked = self.mouse_clicked
                s.hover = True

            self.game_state.update()

            # update and draw sprites
            self.all_sprites.update()
            for z in self.z_layer_groups:
                self.z_layer_groups[z].draw(screen)
            
            # update and draw texts
            [t.update(self) for t in self.all_texts]
            [t.draw(screen) for t in self.all_texts]

            # Limit to 60 frames per second
            clock.tick(60)
        
            # Go ahead and update the screen with what we've drawn.
            game.display.flip()
        
        game.quit()