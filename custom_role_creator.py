import discord
import re

class CustomRoleCreator:
    def __init__(self):
        self.counter = 0
        self.retries = 0
        self.dialog = [
            "\n*We're going to create you a custom role!\nI just need to ask you a few questions.\nSay 'cancel' at anytime to stop the order!\nAre you ready? (yes/no)*",
            "*A custom role costs $3000 to create. Continue? (yes/no)*",
            "*Please enter the name of the role.*",
            "*Please enter the hex color code.*",
            "*Should others be able to purchase this role from the shop? (yes/no)*",
            "*Choose a price between $500-$2500 that others can buy it for.*"
        ]
        self.name = None
        self.color = None
        self.purchasable = None
        self.price = None
        self.done = False
        self.confirmID = None

    def get_response(self, message):
        msg_content = message

        if msg_content == "cancel":
            return 0

        if self.counter == 0:
            if msg_content == "no":
                return 0
            elif msg_content == "yes":
                self.counter += 1
                return 3
            else:
                self.retries += 1
                if self.retries > 2:
                    return 0
                return "Invalid response. Try again."
        elif self.counter == 1:
            if msg_content == "no":
                return 0
            elif msg_content == "yes":
                self.counter += 1
                self.retries = 0
                return 3
            else:
                self.retries += 1
                if self.retries > 2:
                    return 0
                return "Invalid response. Try again."
        elif self.counter == 2:
            self.name = msg_content
            self.counter += 1
            self.retries = 0
            return 3
        elif self.counter == 3:
            str = msg_content
            if str[0] != "#": str = "#" + str
            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str)
            if match:
                self.color = str
                self.counter += 1
                self.retries = 0
                return 3
            else:
                self.retries += 1
                if self.retries > 2:
                    return 0
                return "Invalid response. Try again."
        elif self.counter == 4:
            if msg_content == "no":
                self.purchasable = False
                self.price = "N/A"
                self.done = True
                return 2
            elif msg_content == "yes":
                self.purchasable = True
                self.counter += 1
                self.retries = 0
                return 3
            else:
                self.retries += 1
                if self.retries > 2:
                    return 0
                return "Invalid response. Try again."
        elif self.counter == 5:
            try:
                price = round(float(msg_content), 2)
                if price < 500 or price > 2500:
                    self.retries += 1
                    if self.retries > 2:
                        return 0
                    return "Invalid response. Try again."
                else:
                    self.price = price
                    self.done = True
                    return 2
            except:
                self.retries += 1
                if self.retries > 2:
                    return 0
                return "Invalid response. Try again."
    def get_current(self):
        return self.dialog[self.counter]