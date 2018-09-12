from blackjack.card import Card
from blackjack.deck import Deck
from blackjack.player import Player

deck = Deck(4)

p = Player()
d = Player()

for i in range(2):
    p.addCard(deck.dealNextCard())
    d.addCard(deck.dealNextCard())

print(p.getHand())
print(d.getHand(showFirst=False))

pDone = False
dDone = False
ans = None

while(not pDone or not dDone):
    if not pDone:
        ans = input("hit or stay?").lower()
        if ans == "h":
            pDone = not p.addCard(deck.dealNextCard())
            print(p.getHand())
        else:
            pDone = True

    if not dDone:
        if d.getHandvalue() < 17:
            dDone = not d.addCard(deck.dealNextCard())
            print(d.getHand(showFirst=False))
        else:
            print("The dealer stays")
            dDone = True

    print()

print(p.getHand())
print(d.getHand())

if p.getHandvalue() > d.getHandvalue() and p.getHandvalue() <= 21 or d.getHandvalue() > 21:
    print("You win!")
else:
    print("Dealer wins!")