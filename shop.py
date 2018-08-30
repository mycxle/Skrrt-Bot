import discord
from PIL import Image
import os
import pyimgur


class Shop:
    def __init__(self, db):
        self.db = db
        IMGUR_ID = '36ef56be76e9093'
        self.imgur = pyimgur.Imgur(IMGUR_ID)

    def get_roles(self):
        return list(self.db.child("shop").child("roles").get().val().items())

    def get_role(self, index):
        return self.get_roles()[index]

    def get_roles_embed(self, ctx):
        e = discord.Embed()
        e.colour=discord.Color.green()
        e.title="🚨 ROLES FOR SALE 🚨"
        e.set_thumbnail(url="https://cdn.shopify.com/s/files/1/1061/1924/files/Money_Face_Emoji.png")

        roles = self.get_roles()
        print(roles)
        final_str = ""
        for i in range(len(roles)):
            r = roles[i]
            role = discord.utils.get(ctx.message.server.roles, id=r[0])
            mention = role.mention
            price = "${:.2f}".format(round(float(r[1]), 2))
            final_str += "**{:0>2}** - {} - `{}`".format(i+1, mention, price)
            if r != roles[-1]: final_str += "\n"

        e.description=final_str+"\nmake your own: `>buy role custom`"
        e.set_footer(text='use ">buy role {number}" to purchase!')
        return e

    def get_custom_roles_instructions_embed(self, crc):
        e = discord.Embed()
        e.colour=discord.Colour(int(crc.color[1:], 16))
        e.title="Create this role for $3000?"
        webhexcolor = crc.color
        im = Image.new("RGB", (100,100), webhexcolor)
        PATH = "color.png"
        im.save( PATH)
        uploaded_image = self.imgur.upload_image(PATH, title="Uploaded with PyImgur")
        e.set_thumbnail(url=uploaded_image.link)
        e.add_field(name="Role Name", value=crc.name)
        e.add_field(name="Role Color", value=crc.color)
        e.add_field(name="Purchasable", value=str(crc.purchasable))
        if isinstance(crc.price, str):
            e.add_field(name="Buy Price", value=crc.price)
        else:
            e.add_field(name="Buy Price", value="${:.2f}".format(crc.price))
        e.set_footer(text="👍 to accept | 👎 to cancel")
        return e