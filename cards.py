import board

class Card:
    pass

class LandCard(Card):
    def __init__(self, land):
        self.land = land
        self.land_color = board.LandColor().color(land)

class LandCards:
    def __init__(self):
        self.wheat = 0
        self.brick = 0
        self.sheep = 0
        self.wood = 0
        self.stone = 0

    def AddCardToHand(self, card):
        # WOOD = 1
        # BRICK = 2
        # STONE = 3
        # SHEEP = 4
        # WHEAT = 5
        # DESERT = 6
        # GOLD = 7
        # OCEAN = 8
        # UNKNOWN = -1
        # ANY = -2
        if card.land.value == 1:
            self.wood += 1
        if card.land.value == 2:
            self.brick += 1
        if card.land.value == 3:
            self.stone += 1
        if card.land.value == 4:
            self.sheep += 1
        if card.land.value == 5:
            self.wheat += 1

class DevelopmentCards:
    def __init__(self):
        self.knights = 0
        self.build_roads = 0
        self.draw_cards = 0
        self.monopoly = 0
        self.points = 0