import board

class Card:
    pass

class LandCard(Card):
    def __init__(self, land):
        self.land = land
        self.land_color = board.LandColor().color(land)

class PrintableHand():
    def Print(self):
        pass
    def ConcatEmptyOrPrint(self, c, i, name):
        return c if i == 0 else "{0}, {1} {2}".format(c, i, name)

class LandCards(PrintableHand):
    def __init__(self):
        self.wheat = 0
        self.brick = 0
        self.sheep = 0
        self.wood = 0
        self.stone = 0

    def AddCardsToHand(self, cards):
        for card in cards:
            self.AddCardToHand(card)

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
    
    def Sum(self):
        return self.wood + self.brick + self.stone + self.sheep + self.wheat

    def Print(self):
        # I'm new to python! Surely there is some better way to do this.
        c = self.ConcatEmptyOrPrint("", self.wood, "wood")
        c = self.ConcatEmptyOrPrint(c, self.brick, "brick")
        c = self.ConcatEmptyOrPrint(c, self.stone, "stone")
        c = self.ConcatEmptyOrPrint(c, self.sheep, "sheep")
        c = self.ConcatEmptyOrPrint(c, self.wheat, "wheat")
        return c
    
    def PrintPossibilities(self):
        p = ""
        if self.CanBuildRoad():
            p = "(R)oad"
        if self.CanBuildTown():
            p = p + ", (T)own"
        if self.CanBuildCity():
            p = (p + ", " if p != "" else "") + "(C)ity"
        if self.CanBuyDevCard():
            p = (p + ", " if p != "" else "") + "(D)evelopment card"
        return p
    
    def CanBuildRoad(self):
        return self.wood > 0 and self.brick > 0
    def CanBuildTown(self):
        return self.wood > 0 and self.brick > 0 and self.wheat > 0 and self.sheep > 0
    def CanBuildCity(self):
        return self.stone > 2 and self.wheat > 1
    def CanBuyDevCard(self):
        return self.stone > 0 and self.wheat > 0 and self.sheep > 0

class DevelopmentCards(PrintableHand):
    def __init__(self):
        self.knights = 0
        self.build_roads = 0
        self.draw_cards = 0
        self.monopoly = 0
        self.points = 0
    
    def Print(self):
        # I'm new to python! Surely there is some better way to do this.
        c = self.ConcatEmptyOrPrint("", self.knights, "knights")
        c = self.ConcatEmptyOrPrint(c, self.build_roads, "build_roads")
        c = self.ConcatEmptyOrPrint(c, self.draw_cards, "draw_cards")
        c = self.ConcatEmptyOrPrint(c, self.monopoly, "monopoly")
        c = self.ConcatEmptyOrPrint(c, self.points, "points")
        return c
