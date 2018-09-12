from blackjack.card import Card

class Player:
    def __init__(self):
        self.hand = []

    def addCard(self, card):
        self.hand.append(card)
        return self.getHandvalue()

    def getHand(self, showFirst=True):
        strCards = ""
        for c in self.hand:
            if c is self.hand[0] and not showFirst:
                strCards += "[HIDDEN]\n"
            else: strCards += str(c) + "\n"
        return strCards

    def getHandEmojis(self, showFirst=True):
        emojis = []
        for c in self.hand:
            if c is self.hand[0] and not showFirst:
                emojis.append("card_back")
            else:
                name = Card.strSuits[c.suit][:-1]
                if name.lower() == "club": name = "clover"
                emojis.append(str("card_{}_{}".format(c.number, name)).lower())
        return emojis

    def getHandvalue(self, dealer=False):
        hand = self.hand
        if dealer is True:
            hand = self.hand[1:]
        total = sum(c.value() for c in hand)
        if total > 21:
            aces = (c for c in hand if c.number == 1)
            for a in aces:
                total -= 10
                if total <= 21: break
        return total