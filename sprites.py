import pygame as game
from board import LandColor

class CatanGraphicsDefaults:

    screen_width = 700
    screen_height = 400

    r = 40.0 # main scaler
    e = 1.0 * r

    vert_spacing = 30
    hor_spacing = 30

    def __init__(self):
        self.land_colors = LandColor()

class CatanSprites(game.sprite.Sprite):

    def __init__(self):
        super().__init__()
        WHITE = (255, 255, 255)
        self.defs = CatanGraphicsDefaults()
        self.update_size()
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.color = (255, 0, 0)
        self.clicked = False

    def update_size(self):
        self.image = game.Surface([self.defs.e, self.defs.e])
        self.width = self.defs.e
        self.height = self.defs.e
    
    def draw(self):
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
    
    def has_position(self):
        return not (self.rect.x == self.rect.y == 0)

    # find the position of one of the neighbors and calculate this tile's position from that
    def set_position_from_neighbors(self):
        if self.has_position():
            return True
        
        vert_spacing = CatanGraphicsDefaults.vert_spacing
        hor_spacing = CatanGraphicsDefaults.hor_spacing

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
                return True
        return False

class SWithinTile(CatanSprites):
    
    def __init__(self, color):
        super().__init__()
        
        self.image = game.Surface([self.defs.e, self.defs.e])
        self.image.fill(color)


class STown(SWithinTile):
    
    def __init__(self, player_color, corner):
        super().__init__(player_color)

        self.player_color = player_color
        self.corner = corner

class SCity(SWithinTile):
    
    def __init__(self, stown):
        super().__init__(stown.color)

        self.town

class SBandit(SWithinTile):
    
    def __init__(self, tile):
        super().__init__((0, 0, 0))

class SEdge(CatanSprites):

    def __init__(self, color):
        super().__init__()
        
        self.image = game.Surface([self.defs.e, self.defs.e])
        self.image.fill(color)

class SRoad(SEdge):

    def __init__(self, player_color):
        super().__init__(player_color)
        # eller ändra till self.image.surface.y *= 0.2
        self.image = game.Surface([self.defs.e, self.defs.e * 0.2])

class Text:
    def __init__(self, text, font_name, size):
        self.font = None
        self.surface = None
        self.font_name = font_name
        self.font_size = size
        self.text = text
        self.color = (0, 0, 0)
        self.x = 0
        self.y = 0
    
    def update_text(self, text):
        self.text = text

        if self.font is None:
            self.font = game.font.SysFont(self.font_name, self.font_size)
            self.surface = self.font.render(str(self.text), False, self.color)
        self.surface = self.font.render(str(text), False, self.color)

    def update(self, gameview):
        self.update_text(self.text)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

class MouseText(Text):
    def update(self, gameview):
        self.update_text("{},{}".format(gameview.mouse_x, gameview.mouse_y))

class DieText(Text):
    def __init__(self, stile):
        super().__init__(stile.tile.value, 'Comic Sans MS', 16)
        if stile.tile.value == 6 or stile.tile.value == 8:
            self.color = (255, 0, 0)
        (self.x, self.y) = (stile.rect.x, stile.rect.y)

class KeyState:
    def __init__(self):
        self.keys = None

    def update(self, gameview):
        self.keys = game.key.get_pressed()

# Restart game if R is pressed
class KeyRestartEvent(KeyState):
    def update(self, gameview):
        super().update(gameview)
        if self.keys[game.K_r]:
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

class GameView:
    def __init__(self, starting_state):
        self.defs = CatanGraphicsDefaults()
        # used for drawing the sprites.
        self.all_sprites_list = game.sprite.Group()
        self.mouse_pos = None
        self.mouse_x = None
        self.mouse_y = None
        self.mouse_clicked = False
        self.clicked_sprites = []
        self.all_texts = []
        self.exit_message = ""
        self.game_state = starting_state
    
    def run(self):
        game.init()
        screen = game.display.set_mode([self.defs.screen_width, self.defs.screen_height])
        game.font.init()
        
        keys = [KeyRestartEvent(), KeyQuitEvent()]

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
            [k.update(self) for k in keys]
            
            # set all sprite clicked states
            for s in [s for s in self.all_sprites_list]:
                s.clicked = False
            if self.mouse_clicked:
                for s in [s for s in self.all_sprites_list if s.rect.collidepoint(self.mouse_pos)]:
                    s.clicked = True

            self.game_state.update()

            # update and draw sprites
            self.all_sprites_list.update()
            self.all_sprites_list.draw(screen)

            # update and draw texts
            [t.update(self) for t in self.all_texts]
            [t.draw(screen) for t in self.all_texts]

            # Limit to 60 frames per second
            clock.tick(60)
        
            # Go ahead and update the screen with what we've drawn.
            game.display.flip()
        
        game.quit()