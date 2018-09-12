

class Card:
    strNumbers = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
    strSuits = ["Clubs", "Diamonds", "Spades", "Hearts"]

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __str__(self):
        return Card.strNumbers[self.number-1] + " of " + Card.strSuits[self.suit]

    def value(self):
        if self.number in [11, 12, 13]: return 10
        if self.number is 1: return 11
        return self.number