import board

class Card:
    pass

class LandCard(Card):
    def __init__(self, land):
        self.land = land
        self.land_color = board.LandColor().color(land)