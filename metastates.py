import gamestates


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
        self.players = players
        self.board_stiles = board_stiles
        self.place_town_states = list()
        for player in players + list(reversed(players)):
            place_town = gamestates.PlaceTownState(board_stiles, gameview, player, self)
            self.place_town_states.append(place_town)
            self.place_town_states.append(gamestates.PlaceRoadState(board_stiles, gameview, player, self, place_town.placed_town))
    
    def NextState(self, previous_state):
        if len(self.place_town_states) == 0:
            self.gameview.game_state = MetaPlayerTurn(self.gameview, self.players, self.board_stiles).InitialState()
        else:
            # add initial cards.
            if not self.gameview.game_state.player.cards:
                starting_cards = list()
                for tile in self.gameview.game_state.placed_town.corner.tiles:
                    if tile:
                        starting_cards.append(cards.LandCard(tile.type))
                self.gameview.game_state.player.cards = starting_cards
            self.gameview.game_state = self.ActivateState(self.place_town_states.pop(0))

    def InitialState(self):
        return self.ActivateState(self.place_town_states.pop(0))


class MetaPlayerTurn(MetaState):
    def __init__(self, gameview, players, board_stiles):
        super().__init__(gameview)
        self.players = players
        self.board_stiles = board_stiles
        self.rolled_dice = None

        self.current_player = 0

        self.main_phases = list(map(lambda player: gamestates.PlayerMainPhaseState(board_stiles, gameview, self, player, self.gameview.main_phase_key_events), self.players))
    
    def InitialState(self):
        return self.ActivateState(self.main_phases[self.current_player])
    
    def NextState(self, previous_state):
        # if player won:
        #   game over state

        self.current_player = self.current_player + 1 if self.current_player < len(self.players) - 1 else 0
        return self.InitialState()

    def GetPlayer(self, player_color):
        for p in self.players:
            if p.color == player_color:
                return p
        raise Exception("No player has that color sadly.")