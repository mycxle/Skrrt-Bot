from blackjack.card import Card
from blackjack.deck import Deck
from blackjack.player import Player
import discord

class BlackJack:
    card_emojis = {
        'card_1_clover': '506321744169140226',
        'card_2_heart': '506321744253157377',
        'card_3_spade': '506321744374530054',
        'card_2_spade': '506321744374661122',
        'card_back': '506321744441638922',
        'card_4_diamond': '506321744450027524',
        'card_4_clover': '506321744466935829',
        'card_1_diamond': '506321744479649792',
        'card_1_spade': '506321744575987732',
        'card_2_diamond': '506321744601153536',
        'card_2_clover': '506321744605478912',
        'card_1_heart': '506321744626319360',
        'card_5_heart': '506321744714530817',
        'card_3_diamond': '506321744714530826',
        'card_3_heart': '506321744727113729',
        'card_3_clover': '506321744735371264',
        'card_4_heart': '506321744827645952',
        'card_4_spade': '506321744827777044',
        'card_5_spade': '506321744844423170',
        'card_5_clover': '506321744877846528',
        'card_7_clover': '506321744924114985',
        'card_6_clover': '506321744928309268',
        'card_6_diamond': '506321744932634624',
        'card_5_diamond': '506321744936697856',
        'card_6_heart': '506321745008001024',
        'card_7_heart': '506321745058332673',
        'card_6_spade': '506321745075240980',
        'card_7_diamond': '506321745083629578',
        'card_7_spade': '506321745108795392',
        'card_8_clover': '506321745125441554',
        'card_9_clover': '506321745268047873',
        'card_9_diamond': '506321745368580117',
        'card_9_spade': '506321745377230850',
        'card_8_diamond': '506321745414979594',
        'card_10_clover': '506321745456922626',
        'card_10_spade': '506321745456922635',
        'card_8_spade': '506321745561649162',
        'card_8_heart': '506321745586946048',
        'card_9_heart': '506321745595334667',
        'card_10_diamond': '506321745758912512',
        'card_10_heart': '506321745779752969',
        'card_11_heart': '506321745817370636',
        'card_11_clover': '506321745821564969',
        'card_13_heart': '506321745880547329',
        'card_11_diamond': '506321745968365571',
        'card_12_spade': '506321746002051072',
        'card_12_clover': '506321746006245376',
        'card_12_heart': '506321746006376468',
        'card_11_spade': '506321746018697226',
        'card_13_spade': '506321746023022622',
        'card_13_diamond': '506321746027216906',
        'card_13_clover': '506321746035736576',
        'card_12_diamond': '506321746077548544',
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

        self.firstTurnDone = False
        self.surrendered = False
        self.doubled = False

    def surrender(self):
        self.surrendered = True
        self.pDone = True
        self.dDone = True

    def double(self):
        self.doubled = True
        self.hit()
        self.pDone = True
        self.bet *= 2
        self.done()

    def set_message(self, msg):
        self.msg = msg

    def hit(self):
        self.firstTurnDone = True
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
                if self.p.getHandvalue() == 21 and self.firstTurnDone is False:
                    the_bet *= 2
                e.set_author(name="{}#{} - YOU WON! [+${:.2f}]".format(self.user.name, self.user.discriminator, the_bet), icon_url=self.user.avatar_url)
            elif winner == 1:
                loseMsg = "YOU LOST!"
                theBet = self.bet
                if self.surrendered is True:
                    loseMsg = "SURRENDERED!"
                    theBet /= 2.0
                e.set_author(name="{}#{} - {} [-${:.2f}]".format(self.user.name, self.user.discriminator, loseMsg, theBet), icon_url=self.user.avatar_url)
                e.colour=discord.Color.red()
            else:
                loseMsg = "STANDOFF!"
                e.set_author(name="{}#{} - {} [$0.00]".format(self.user.name, self.user.discriminator, loseMsg), icon_url=self.user.avatar_url)
                e.colour=discord.Color.purple()

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
        #e.description="**Dealer has an Ace. __Buy Insurance?__** - ℹ️"
        e.set_footer(text="▶️ = hit ⏹ = stand ⏩ = double ⏏️ = surrender")
        self.e = e
        return self.e

    def done(self):
        self.firstTurnDone = True
        self.pDone = True
        while self.dDone is False:
            self.dealer_turn()

    def dealer_turn(self):
        if not self.dDone:
            if self.p.getHandvalue() > 21:
                self.dDone = True
                return
            if self.d.getHandvalue() < self.p.getHandvalue() or (self.d.getHandvalue() == self.p.getHandvalue() and self.d.getHandvalue() < 17):
                self.d.addCard(self.deck.dealNextCard())
                self.dbust = self.d.getHandvalue() > 21
            else:
                self.dDone = True
        return self.dbust

    def is_over(self):
        return self.pDone and self.dDone

    def who_won(self):
        if self.surrendered:
            return 1
        if self.p.getHandvalue() > 21:
            return 1
        if self.p.getHandvalue() > self.d.getHandvalue() and self.p.getHandvalue() <= 21 or self.d.getHandvalue() > 21:
            return 0
        elif self.p.getHandvalue() == self.d.getHandvalue():
            return 2
        else:
            return 1