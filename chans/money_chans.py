import asyncio
from globals import Global
from timex import Timer


class MoneyChans:
    def __init__(self):
        self.bad_ids = Global.security.get("nomoney_channels")

    @asyncio.coroutine
    async def on_message(self, bot, message):
        msg_content = message.content
        author = message.author
        money = Global.money

        if message.channel.id in self.bad_ids:
            return

        if author.id not in money.moneycooldowns and not msg_content.startswith(Global.bot_prefix) and not author.bot:
            amount = money.get_money()
            money.deposit(author.id, amount)
            money.moneycooldowns.append(message.author.id)
            Timer(60, money.remove_money_cooldown, message.author.id)
        else:
            print("already in cooldowns")
