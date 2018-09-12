import random
from blackjack.card import Card

class Deck:
    def __init__(self, numDecks, shuffle=True):
        self.cards = list()

        for d in range(numDecks):
            for s in range(4):
                for n in range(1, 14):
                    self.cards.append(Card(s, n))

        if shuffle:
            random.shuffle(self.cards)

    def dealNextCard(self):
        return self.cards.pop(0)

    def printDeck(self):
        for c in self.cards:
            print(c)