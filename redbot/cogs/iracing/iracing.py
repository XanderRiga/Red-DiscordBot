from redbot.core import commands
import os
import sys
import dotenv
from .ir_webstats_rc.client import iRWebStats
from .ir_webstats_rc.responses.last_races_stats import LastRacesStats

dotenv.load_dotenv()

irw = iRWebStats()
irw.login(os.getenv("IRACING_USERNAME"), os.getenv("IRACING_PASSWORD"))


class Iracing(commands.Cog):
    """A cog that can give iRacing data about users"""

    @commands.command()
    async def recentraces(self, ctx, *, iracing_id):
        """Gives the recent race data from the iRacing ID they passed in"""
        response = irw.lastrace_stats(iracing_id)

        races_stats_list = map(lambda x: LastRacesStats(x), response)

        await ctx.send(print_recent_races(races_stats_list, iracing_id))


def print_recent_races(recent_races, iracing_id):
    string = 'Recent Races Data for user: ' + str(iracing_id) + '\n\n'
    string += 'Finish'.ljust(8) + \
              'Start'.ljust(8) + \
              'Incidents'.ljust(11) + \
              'Race Date'.ljust(15) + \
              'Track Name'.ljust(30) + '\n'
    string += '---------------------------------------------------------------------------------\n'

    for recent_race in recent_races:
        string += 'P' + str(recent_race.finishPos).ljust(8) + \
                  'P' + str(recent_race.startPos).ljust(8) + \
                  str(recent_race.incidents).ljust(11) + \
                  recent_race.date.ljust(15) + \
                  recent_race.trackName.ljust(30) + '\n'

    return add_backticks(string)


def add_backticks(string):
    return '```' + string + '```'
