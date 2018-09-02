import discord
import re
import textwrap

class CustomRoleCreator:
    def __init__(self):
        self.colornames = {
            "teal" : 0x1abc9c,
            "dark teal" : 0x11806a,
            "green" : 0x2ecc71,
            "dark green" : 0x1f8b4c,
            "blue" : 0x3498db,
            "dark blue" : 0x206694,
            "purple" : 0x9b59b6,
            "dark purple" : 0x71368a,
            "magenta" : 0xe91e63,
            "dark magenta" : 0xad1457,
            "gold" : 0xf1c40f,
            "dark gold" : 0xc27c0e,
            "orange" : 0xe67e22,
            "dark orange" : 0xa84300,
            "red" : 0xe74c3c,
            "dark red" : 0x992d22,
            "lighter grey" : 0x95a5a6,
            "dark grey" : 0x607d8b,
            "light grey" : 0x979c9f,
            "darker grey" : 0x546e7a,
            "black" : 0x010101,
            "white" : 0xffffff
        }

        self.counter = 0
        self.retries = 0
        self.dialog = [
            "\n*We're going to create you a custom role!\nI just need to ask you a few questions.\nSay 'cancel' at anytime to stop the order!\nAre you ready? (yes/no)*",
            "*A custom role costs $3000 to create. Continue? (yes/no)*",
            "*Please enter the name of the role.*",
            "*Please enter the hex color code.*\n*__or choose one of the following colors:__*\n" + textwrap.fill(", ".join(self.colornames), 55),
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

        if msg_content.lower() == "cancel":
            return 0

        if self.counter == 0:
            msg_content = msg_content.lower()
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
            msg_content = msg_content.lower()
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
            if "gray" in str: str = str.replace("gray", "grey")
            if str.lower() in self.colornames:
                str = "#" + '{0:06X}'.format(self.colornames[str.lower()])
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
            msg_content = msg_content.lower()
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