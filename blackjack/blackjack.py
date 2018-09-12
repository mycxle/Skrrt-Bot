from blackjack.card import Card
from blackjack.deck import Deck
from blackjack.player import Player
import discord

class BlackJack:
    card_emojis = {
        'card_1_clover':'486716058254704641',
        'card_2_clover':'486716058259161099',
        'card_5_clover':'486716058401767455',
        'card_3_clover':'486716058452099073',
        'card_4_clover':'486716058670202900',
        'card_9_clover':'486716058703495172',
        'card_7_clover':'486716058766540801',
        'card_8_clover':'486716058817003521',
        'card_11_clover':'486716058846232591',
        'card_10_clover':'486716058879918083',
        'card_6_clover':'486716058946895908',
        'card_12_clover':'486716059437629450',
        'card_13_clover':'486716059471314954',
        'card_3_diamond':'486716196331323403',
        'card_6_diamond':'486716196381786136',
        'card_4_diamond':'486716196474060835',
        'card_1_diamond':'486716196511678474',
        'card_2_diamond':'486716196582981642',
        'card_5_diamond':'486716196599758858',
        'card_9_diamond':'486716196633313281',
        'card_7_diamond':'486716196658479114',
        'card_12_diamond':'486716196662542337',
        'card_8_diamond':'486716196725587998',
        'card_11_diamond':'486716196855611412',
        'card_10_diamond':'486716196956143616',
        'card_13_diamond':'486716196960600075',
        'card_1_heart':'486716249896779786',
        'card_3_heart':'486716249900974110',
        'card_2_heart':'486716250194575370',
        'card_4_heart':'486716250261684224',
        'card_5_heart':'486716250412548106',
        'card_6_heart':'486716250525794314',
        'card_7_heart':'486716250605617162',
        'card_8_heart':'486716250760806400',
        'card_9_heart':'486716250790297600',
        'card_10_heart':'486716250932772874',
        'card_11_heart':'486716250953875457',
        'card_13_heart':'486716251020984351',
        'card_12_heart':'486716251201339423',
        'card_1_spade':'486716316561047568',
        'card_2_spade':'486716317525868546',
        'card_4_spade':'486716317693378561',
        'card_3_spade':'486716317848567809',
        'card_5_spade':'486716318641291265',
        'card_6_spade':'486716318889017354',
        'card_7_spade':'486716319031361546',
        'card_8_spade':'486716319098470400',
        'card_9_spade':'486716319199264769',
        'card_10_spade':'486716319434014741',
        'card_11_spade':'486716319652380693',
        'card_12_spade':'486724793379323921',
        'card_13_spade':'486724793882771466',
        'card_back':'489199274693754882'
    }

    def __init__(self, bot, user, bet):
        self.bot = bot
        self.user = user
        self.bet = bet
        self.deck = Deck(4)
        self.p = Player()
        self.d = Player()
        self.dbust = False

        for i in range(2):
            self.p.addCard(self.deck.dealNextCard())
            self.d.addCard(self.deck.dealNextCard())

        self.pDone = False
        self.dDone = False
        self.ans = None
        if self.p.getHandvalue() == 21:
            print("21")
            self.dDone = True
            self.pDone = True

    def hit(self):
        if not self.pDone:
            self.p.addCard(self.deck.dealNextCard())
            print(str(self.p.getHandvalue()))
            self.pDone = self.p.getHandvalue() >= 21
        return self.pDone

    def create_embed(self, winEmbed=False):
        e = discord.Embed()

        if winEmbed is False:
            e.colour=discord.Color.blue()
            e.set_author(name="{}#{}".format(self.user.name, self.user.discriminator), icon_url=self.user.avatar_url)
        else:
            winner = self.who_won()
            if winner == 0:
                e.colour=discord.Color.green()
                the_bet = self.bet
                if self.p.getHandvalue() == 21 and len(self.p.hand) == 2:
                    the_bet *= 2
                e.set_author(name="{}#{} - YOU WON! [+${:.2f}]".format(self.user.name, self.user.discriminator, the_bet), icon_url=self.user.avatar_url)
            else:
                e.set_author(name="{}#{} - YOU LOST! [-${:.2f}]".format(self.user.name, self.user.discriminator, self.bet), icon_url=self.user.avatar_url)
                e.colour=discord.Color.red()

        pValue = str(self.p.getHandvalue()) + " `"
        if winEmbed is False:
            dValue = str(self.d.getHandvalue(dealer=True)) + " `"
        else:
            dValue = str(self.d.getHandvalue()) + " `"

        pDisplay = []
        for card in self.p.hand:
            number = card.number
            display = str(number)

            if card.number == 1: display = "A"
            if card.number == 11: display = "J"
            if card.number == 12: display = "Q"
            if card.number == 13: display = "K"

            pDisplay.append(display)

        dDisplay = []
        for card in self.d.hand:
            number = card.number
            display = str(number)

            if card.number == 1: display = "A"
            if card.number == 11: display = "J"
            if card.number == 12: display = "Q"
            if card.number == 13: display = "K"

            dDisplay.append(display)

        if winEmbed is False:
            dDisplay = dDisplay[1:]
            ddValue = "?, " + ", ".join(dDisplay) + " = ` "
        else:
            ddValue = "" + ", ".join(dDisplay) + " = ` "

        pdValue = "" + ", ".join(pDisplay) + " = ` "



        pE = self.p.getHandEmojis()

        if winEmbed is False:
            dE = self.d.getHandEmojis(showFirst=False)
        else:
            dE = self.d.getHandEmojis()


        pEmojis = []

        for em in pE:
            pEmojis.append("<:{}:{}>".format(em, BlackJack.card_emojis[em]))

        dEmojis = []
        for em in dE:
            dEmojis.append("<:{}:{}>".format(em, BlackJack.card_emojis[em]))

        print(pEmojis)
        print(dEmojis)

        print("Player cards: " + self.p.getHand())
        print("Dealers cards: " + self.d.getHand(showFirst=False))

        e.add_field(name="**Your Hand:**", value=" ".join(pEmojis)+"\n"+pdValue+pValue)
        e.add_field(name="**Dealer Hand:**", value=" ".join(dEmojis)+"\n"+ddValue+dValue)
        e.set_footer(text="▶️ = hit ⏹ = stand ⏩ = double down 🔀 = split")
        self.e = e
        return self.e

    def done(self):
        self.pDone = True
        while self.dDone is False:
            self.dealer_turn()

    def dealer_turn(self):
        if not self.dDone:
            if self.p.getHandvalue() > 21:
                self.dDone = True
                return
            if self.d.getHandvalue() < 17:
                self.d.addCard(self.deck.dealNextCard())
                self.dbust = self.d.getHandvalue() > 21
            else:
                self.dDone = True
        return self.dbust

    def is_over(self):
        return self.pDone and self.dDone

    def who_won(self):
        if self.p.getHandvalue() > 21:
            return 1
        if self.p.getHandvalue() > self.d.getHandvalue() and self.p.getHandvalue() <= 21 or self.d.getHandvalue() > 21:
            return 0
        else:
            return 1