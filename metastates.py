import gamestates
import sprites
import cards

class MetaState():
    def __init__(self, gameview):
        self.gameview = gameview
    
    def NextState(self, previous_state):
        self.gameview.game_state = None

    def InitialState(self):
        return None # override this and return AcivateState(<next state>)

    def ActivateState(self, state):
        state.ActivateState()
        self.gameview.game_state = state

# Opening of the game - each player places one town each etc.
class MetaPlaceInitialTowns(MetaState):
    def __init__(self, gameview, players, board_stiles):
        super().__init__(gameview)
        self.players = players
        self.board_stiles = board_stiles
        self.place_town_states = list()
        for player in players + list(reversed(players)):
            place_town = gamestates.PlaceTownState(board_stiles, gameview, player, self, False)
            self.place_town_states.append(place_town)
            self.place_town_states.append(gamestates.PlaceRoadState(board_stiles, gameview, player, self, place_town.placed_town))
    
    def NextState(self, previous_state):
        if len(self.place_town_states) == 0:
            # If all initial towns are placed, activate the main player turn states.
            self.ActivateState(MetaPlayerTurn(self.gameview, self.players, self.board_stiles).InitialState())
        else:
            # add initial cards.
            if self.gameview.game_state.player.cards.Sum() == 0:
                starting_cards = list()
                for tile in self.gameview.game_state.placed_town.corner.tiles:
                    if tile:
                        starting_cards.append(cards.LandCard(tile.type))
                self.gameview.game_state.player.cards.AddCardsToHand(starting_cards)
            self.ActivateState(self.place_town_states.pop(0))

    def InitialState(self):
        return self.ActivateState(self.place_town_states.pop(0))

# This meta state handles the normal game turn order.
class MetaPlayerTurn(MetaState):
    def __init__(self, gameview, players, board_stiles):
        super().__init__(gameview)
        self.players = players
        self.board_stiles = board_stiles
        self.rolled_dice = None
        self.triggered_action_state = None

        self.current_player = 0
        self.current_hand_text = sprites.Text('current hand', 'Comic Sans MS', 20)
        (self.current_hand_text.x, self.current_hand_text.y) = (36, 600)
        self.gameview.all_texts.append(self.current_hand_text)

        self.main_phases = list(map(lambda player: gamestates.PlayerMainPhaseState(board_stiles, gameview, self, player, self.gameview.main_phase_key_events), self.players))
    
    def InitialState(self):
        return self.main_phases[self.current_player]

    def NextState(self, previous_state):
        if self.triggered_action_state:
            self.triggered_action_state.DeactivateState()
            self.triggered_action_state = None
            self.ActivateState(self.InitialState())
        else:
            # if player won:
            #   game over state

            self.main_phases[self.current_player].DeactivateState()
            self.main_phases[self.current_player - 1 if self.current_player > 0 else len(self.players) - 1].DeactivateState()
            self.current_player = self.current_player + 1 if self.current_player < len(self.players) - 1 else 0
            self.ActivateState(self.InitialState())
    
    def TriggerPlayerActionState(self, state):
        self.triggered_action_state = state
        self.ActivateState(state)

    def GetPlayer(self, player_color):
        for p in self.players:
            if p.color == player_color:
                return p
        raise Exception("No player has that color sadly.")