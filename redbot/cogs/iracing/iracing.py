from redbot.core import commands


class Iracing(commands.Cog):
    """A cog that can give iRacing data about users in the discord"""

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")
