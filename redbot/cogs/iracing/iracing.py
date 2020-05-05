from redbot.core import commands
import os
import sys
import dotenv
from .ir_webstats_rc.client import iRWebStats
from .ir_webstats_rc.responses.last_races_stats import LastRacesStats
from .ir_webstats_rc.responses.yearly_stats import YearlyStats
from .ir_webstats_rc.responses.career_stats import CareerStats
from .storage import *
import copy

dotenv.load_dotenv()

irw = iRWebStats()
irw.login(os.getenv("IRACING_USERNAME"), os.getenv("IRACING_PASSWORD"))


class Iracing(commands.Cog):
    """A cog that can give iRacing data about users"""

    @commands.command()
    async def recentraces(self, ctx, *, iracing_id=None):
        """Gives the recent race data from the iRacing ID passed in"""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if not iracing_id:
            iracing_id = get_user_iracing_id(user_id, guild_id)
            if not iracing_id:
                await ctx.send('Please send an iRacing ID after the command or link your own with `!saveid <iRacing '
                               'ID>`')
                return

        response = irw.lastrace_stats(iracing_id)

        races_stats_list = map(lambda x: LastRacesStats(x), response)

        update_user(user_id, guild_id, None, None, copy.deepcopy(races_stats_list))

        await ctx.send(print_recent_races(races_stats_list, iracing_id))

    @commands.command()
    async def yearlystats(self, ctx, *, iracing_id=None):
        """Gives the yearly data from the iRacing ID passed in"""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if not iracing_id:
            iracing_id = get_user_iracing_id(user_id, guild_id)
            if not iracing_id:
                await ctx.send('Please send an iRacing ID after the command or link your own with `!saveid <iRacing '
                               'ID>`')
                return

        response = irw.yearly_stats(iracing_id)

        yearly_stats = map(lambda x: YearlyStats(x), response)

        update_user(user_id, guild_id, None, copy.deepcopy(yearly_stats), None)

        await ctx.send(print_yearly_stats(yearly_stats, iracing_id))

    @commands.command()
    async def careerstats(self, ctx, *, iracing_id=None):
        """Gives the career data from the iRacing ID passed in"""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        if not iracing_id:
            iracing_id = get_user_iracing_id(user_id, guild_id)
            if not iracing_id:
                await ctx.send('Please send an iRacing ID after the command or link your own with `!saveid <iRacing '
                               'ID>`')
                return

        response = irw.career_stats(iracing_id)

        career_stats = map(lambda x: CareerStats(x), response)

        update_user(user_id, guild_id, copy.deepcopy(career_stats), None, None)

        await ctx.send(print_career_stats(career_stats, iracing_id))

    @commands.command()
    async def saveid(self, ctx, *, iracing_id):
        """Save your iRacing ID with to your Discord ID"""

        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)

        save_iracing_id(user_id, guild_id, iracing_id)

        await ctx.send('iRacing ID successfully saved')


def print_career_stats(career_stats, iracing_id):
    string = 'Career Data for user: ' + str(iracing_id) + '\n\n'
    string += 'Category'.ljust(10) + \
              'Starts'.ljust(8) + \
              'Top 5s'.ljust(8) + \
              'Wins'.ljust(8) + \
              'Avg Start'.ljust(12) + \
              'Avg Finish'.ljust(12) + \
              'Avg Incidents'.ljust(15) + \
              'Top 5 Percentage'.ljust(18) + \
              'Win Percentage'.ljust(16) + '\n'
    string += '--------------------------------------------------------------------' \
              '---------------------------------------------\n'

    for career_stat in career_stats:
        string += career_stat.category.ljust(10) + \
                  str(career_stat.starts).ljust(8) + \
                  str(career_stat.top5).ljust(8) + \
                  str(career_stat.wins).ljust(8) + \
                  str(career_stat.avgStart).ljust(12) + \
                  str(career_stat.avgFinish).ljust(12) + \
                  str(career_stat.avgIncPerRace).ljust(15) + \
                  str(career_stat.top5Percentage).ljust(18) + \
                  str(career_stat.winPercentage).ljust(16) + '\n'

    return add_backticks(string)


def print_yearly_stats(yearly_stats, iracing_id):
    string = 'Yearly Data for user: ' + str(iracing_id) + '\n\n'
    string += 'Year'.ljust(6) + \
              'Category'.ljust(10) + \
              'Starts'.ljust(8) + \
              'Top 5s'.ljust(8) + \
              'Wins'.ljust(8) + \
              'Avg Start'.ljust(12) + \
              'Avg Finish'.ljust(12) + \
              'Avg Incidents'.ljust(15) + \
              'Top 5 Percentage'.ljust(18) + \
              'Win Percentage'.ljust(16) + '\n'
    string += '--------------------------------------------------------------------' \
              '---------------------------------------------\n'

    for yearly_stat in yearly_stats:
        string += str(yearly_stat.year).ljust(6) + \
                  yearly_stat.category.ljust(10) + \
                  str(yearly_stat.starts).ljust(8) + \
                  str(yearly_stat.top5).ljust(8) + \
                  str(yearly_stat.wins).ljust(8) + \
                  str(yearly_stat.avgStart).ljust(12) + \
                  str(yearly_stat.avgFinish).ljust(12) + \
                  str(yearly_stat.avgIncPerRace).ljust(15) + \
                  str(yearly_stat.top5Percentage).ljust(18) + \
                  str(yearly_stat.winPercentage).ljust(16) + '\n'

    return add_backticks(string)


def print_recent_races(recent_races, iracing_id):
    string = 'Recent Races Data for user: ' + str(iracing_id) + '\n\n'
    string += 'Finish'.ljust(8) + \
              'Start'.ljust(8) + \
              'Incidents'.ljust(11) + \
              'Avg iRating'.ljust(13) + \
              'Race Date'.ljust(15) + \
              'Track Name'.ljust(30) + '\n'
    string += '---------------------------------------------------------------------------------\n'

    for recent_race in recent_races:
        string += ('P' + str(recent_race.finishPos)).ljust(8) + \
                  ('P' + str(recent_race.startPos)).ljust(8) + \
                  str(recent_race.incidents).ljust(11) + \
                  str(recent_race.strengthOfField).ljust(13) + \
                  recent_race.date.ljust(15) + \
                  recent_race.trackName.ljust(30) + '\n'

    return add_backticks(string)


def add_backticks(string):
    return '```' + string + '```'
