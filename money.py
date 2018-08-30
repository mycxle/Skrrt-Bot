import random
import asyncio

class Money:
    def __init__(self, db):
        self.moneycooldowns = []
        self.db = db

    def get_money(self):
        return round(random.uniform(0.1, 1), 2)

    def get_math_money(self):
        return round(random.uniform(0.05, 0.3), 2)

    @asyncio.coroutine
    async def remove_money_cooldown(self, id):
        self.moneycooldowns.remove(id)

    def get_user(self, id):
        user = self.db.child("money").child(id).get().val()

        if user is None:
            user = self.db.child("money").child(id).set({"balance": "0", "last_daily": "..."})

        return user

    def deposit(self, id, amount):
        if amount <= 0:
            raise Exception("deposit amount must be positive!")

        user = self.get_user(id)

        balance = float(user["balance"])
        balance += amount
        last_daily = user["last_daily"]
        self.db.child("money").child(id).set({"balance": str(round(balance, 2)), "last_daily": last_daily})

    def withdraw(self, id, amount):
        if amount <= 0:
            raise Exception("withdraw amount must be positive!")

        user = self.get_user(id)

        balance = float(user["balance"])
        balance -= amount
        last_daily = user["last_daily"]
        self.db.child("money").child(id).set({"balance": str(round(balance, 2)), "last_daily": last_daily})