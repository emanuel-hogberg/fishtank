import sprites
import random

class GameState:
    def __init__(self, board_stiles, gameview, meta_state):
        self.stiles = board_stiles
        self.tiles = list(map(lambda s: s.tile, self.stiles))
        self.gameview = gameview
        self.z_mid = list(filter(lambda z: z.name == "Constructs", self.gameview.z_layers))[0]
        self.z_front = list(filter(lambda z: z.name == "Front", self.gameview.z_layers))[0]
        self.meta_state = meta_state
    
    def ActivateState(self):
        pass

class MetaState():
    def __init__(self, gameview):
        self.gameview = gameview
    
    def NextState(self, previous_state):
        self.gameview.game_state = None

    def InitialState(self):
        return None # override this and return AcivateState(<next state>)

    def ActivateState(self, state):
        state.ActivateState()
        return state

# Opening of the game - each player places one town each etc.
class MetaPlaceInitialTowns(MetaState):
    def __init__(self, gameview, players, board_stiles):
        super().__init__(gameview)
        self.place_town_states = list()
        for player in players + list(reversed(players)):
            self.place_town_states.append(PlaceTownState(board_stiles, gameview, player, self))
            #self.place_town_states.append(PlaceRoadState(board_stiles, gameview, player, self))
    
    def NextState(self, previous_state):
        if len(self.place_town_states) == 0:
            raise NotImplementedError("Oh no only possible to place initial towns atm pls")
        self.gameview.game_state = self.ActivateState(self.place_town_states.pop(0))

    def InitialState(self):
        return self.ActivateState(self.place_town_states.pop(0))

class PlaceTownState(GameState):
    def __init__(self, board_stiles, gameview, player, meta_state):
        super().__init__(board_stiles, gameview, meta_state)
        self.player = player
        
        self.pointer = None
        self.status_text = None
    
    def ActivateState(self):
        self.pointer = sprites.SPointer()
        self.gameview.AddSprite(self.pointer, self.z_front)

        self.status_text = sprites.Text('{} please place a town'.format(self.player.name), 'Comic Sans MS', 30)
        self.status_text.color = self.player.color
        (self.status_text.x, self.status_text.y) = (230, 3)
        self.gameview.all_texts.append(self.status_text)        

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
                # self.status_text.update_text("{} [] {}, {} corners".format(
                #     stile.tile.name, stile.tile.value,
                #     sum(map(lambda c: 0 if c is None else 1, stile.tile.corners))))
                
                # clicked?
                if stile.clicked:
                    if self.LocationAcceptable(stile, closest_corner):
                        self.gameview.AddSprite(sprites.STown(self.player.color, closest_corner), self.z_mid)
                        self.pointer.removed = True
                        self.status_text.removed = True
                        self.meta_state.NextState(self)
                    else:
                        self.status_text.text = "Oh no, location not legal. try again pls"
        else:
            self.pointer.hide = True
            # self.status_text.update_text('-')
    def LocationAcceptable(self, stile, corner):
        for n in corner.neighbor_corners:
            if not n.town is None:
                return False
        return True
        

class Player:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.cards = list()
        self.dev_cards = list()
        self.score = 0
        self.ai = None

class Scores:
    def __init__(self, players):
        self.players = players
        self.towns = list()
        self.player_with_longest_road = None
        self.player_with_largest_army = None
    
    def RandomStartingPlayer(self):
        starting_player = self.players[random.randint(0, len(self.players) - 1)]
        while self.players[0] != starting_player:
            self.players.append(self.players.pop(0))
        return starting_player

    # work in progress
    def CountScores(self):
        for player in self.players:
            player.score = len(list(filter(lambda town: town.player == player, self.towns))) + \
                2 * len(list(filter(lambda town: town.is_city and town.player == player, self.towns))) + \
                len(list(filter(lambda card: card == "1", player.dev_cards)))