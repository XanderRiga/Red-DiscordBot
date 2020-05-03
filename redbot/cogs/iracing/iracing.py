from redbot.core import commands
import os
import sys
import dotenv
from .ir_webstats_rc.client import iRWebStats
dotenv.load_dotenv()


class Iracing(commands.Cog):
    """A cog that can give iRacing data about users in the discord"""

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""

        irw = iRWebStats()
        irw.login(os.getenv("IRACING_USERNAME"), os.getenv("IRACING_PASSWORD"))

        print(irw.lastrace_stats("499343"))

        await ctx.send("I can do stuff!")
