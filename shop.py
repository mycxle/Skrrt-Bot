import discord

class Shop:
    def __init__(self, db):
        self.db = db

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
            if r != roles[-1]: str += "\n"

        e.description=final_str
        e.set_footer(text='use ">buy role {number}" to purchase!')
        return e