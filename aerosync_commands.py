from typing import Literal
import discord
from discord import app_commands

from custom_types import Phase
import database
from votes import get_votecount

def is_host(interaction: discord.Interaction) -> bool:
  for role in interaction.user.roles:
    if (role.name in ["Mafia", "Puppeteer (Host)", "God"]):
      return True
  return False

def is_developer(interaction: discord.Interaction) -> bool:
  for role in interaction.user.roles:
    if (role.name in ["God"]):
      return True
  return False

help_message = discord.Embed(colour=discord.Color.teal(),
                             description="""**Commands:**
                            `/alias add <name> <alias>` - Add an alias for a player.
                            `/alias list` - List all aliases.

                            `/game url <game> <url>` - Set the URL for a game.
                            `/game scrape_playerlist <game>` - Populate list of living players.

                            `/update toggle <game> <on/off>` - Toggle updates on or off.
                            `/update interval <game> <interval>` - Set the interval for updating posts.
                            `/update now <game>` - Request an immediate update.

                            `/game_phase add <game> <phase> <postnum>` - Add a phase to a game.
                            `/game_phase remove <game> <phase_name>` - Remove a phase from a game.
                            `/game_phase list <game>` - List all phases for a game.

                            `/votecount get_retrospective <game> <postnum>` - Get retrospective votecount.
                            `/votecount get_current <game>` - Get current votecount.
                            `/votecount list` - List all aliases.

                            `/rank_activity all <game>` - Rank activity for all time.
                            `/rank_activity today <game>` - Rank activity for today.

                            `/special help` - Display this help message.
                            `/special ping` - Check if the bot is still running.
                            `/special web` - Give link to web interface.

                             Accurate votecounts rely on maintaining the list of living players. [Spreadsheet link](https://docs.google.com/spreadsheets/d/1nEDOQnXse2B5DZktZmmJKolFNLpkFFbLURNQdtPyS3Q/edit?usp=sharing)
                             """)

#DEVELOPER COMMANDS - RESTRICTED USE (God)
class god(app_commands.Group):
    #Wipe the entire database and reset to factory defaults
    @app_commands.command()
    @app_commands.check(is_developer)
    async def factory_reset(self, interaction: discord.Interaction):
        database.clear_db_factory_defaults()
        await interaction.response.send_message('Factory reset complete. All games wiped and reset to factory defaults.')

#MOD COMMANDS - RESTRICTED USE  (Host, Puppeteer, God)
class game(app_commands.Group):
    #set game URL and wipe the database for that game
    @app_commands.command()
    @app_commands.check(is_host)
    @app_commands.describe(game='Available Games', url="game url")
    async def url(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C'], url: str):
        database.wipe_game_db(game)
        #sample urls
        #https://hypixel.net/threads/hypixel-mafia-lxxv-pokemon-mafia-upick-day-2.5718601/
        #https://hypixel.net/threads/hypixel-mafia-lxxv-pokemon-mafia-upick-day-5.5718601/page-345

        #if it's the first, we need to add page-1 to the end
        #if it's the second, we need to remvoe the page-3 from the end (so it ends in page-)
        #use a regex to figure out which one it is
        if url[-1] == "/":
            url += "page-"
        else:
            #remove the page number, arbitrarily length
            url = url[:url.rfind("page-")] + "page-"
            database.set_game_attr(game, "url", url)

        await interaction.response.send_message(
            'Wiped post database and Set url for game {} to {}.'.format(game, url))
        
    #populate list of living players
    @app_commands.command()
    @app_commands.check(is_host)
    @app_commands.describe(game='Available Games')
    async def scrape_playerlist(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C']):
        database.scrape_playerlist(game)
        await interaction.response.send_message('Scraped playerlist for game {}.'.format(game))


class update(app_commands.Group):
    #toggle updates on or off
    @app_commands.command()
    @app_commands.check(is_host)
    @app_commands.describe(game='Available Games', toggle="on or off")
    async def toggle(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C'], toggle: Literal['on', 'off']):
        if toggle == "on":
            database.set_game_attr(game, "update_toggle", True)
            await interaction.response.send_message('Set update toggle for game **{}** to **{}**. Update interval is currently set to **{}** minutes. Remember to update the phases!'.format(game, database.get_game_attr('A', toggle, 'interval')))
        if toggle == "off":
            database.set_game_attr(game, "update_toggle", False)
            await interaction.response.send_message('Set update toggle for game **{}** to **{}**.'.format(game, toggle))

    #set interval for updating posts
    @app_commands.command()
    @app_commands.check(is_host)
    @app_commands.describe(game='Available Games', interval="interval in minutes")
    async def interval(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C'], interval: int):
        database.set_game_attr(game, "interval", interval)

        await interaction.response.send_message('Set interval for game **{}** to **{}** minutes.'.format(game, interval))

    #DATABASE COMMANDS - PUBLIC USE

    #Immediate update request
    @app_commands.command()
    @app_commands.describe(game='Available Games')
    async def now(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C']):
        database.set_game_attr(game, "update_now_requested", True)

        await interaction.response.send_message('Immediate update requested for game {}. Updating typically takes a minute.'.format(game))


class game_phase(app_commands.Group):
    #set phase for a game
    @app_commands.command()
    @app_commands.check(is_host)
    @app_commands.describe(game='Available Games', phase="Phase", postnum="Post number")
    async def add(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C'], phase: str, postnum: int):
        database.add_phase_to_db(game, Phase(postnum, phase))

        await interaction.response.send_message('Added phase {} for game {} at post number {}.'.format(phase, game, postnum))

    #remove phase for a game
    @app_commands.command()
    @app_commands.check(is_host)
    @app_commands.describe(game='Available Games', phase_name="Phase name")
    async def remove(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C'], phase_name: str):
        database.remove_phase_from_db(game, phase_name)

        await interaction.response.send_message('Removed phase {} from game {}.'.format(phase_name, game))

    #list phases for a game
    @app_commands.command()
    @app_commands.check(is_host)
    @app_commands.describe(game='Available Games')
    async def list(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C']):
        phases = database.get_phases(game)
        text = "**Phases for game {}:**\n".format(game)
        for phase in phases:
            text += "{}: {}\n".format(phase['phase'], phase['postnum'])
        embed = discord.Embed(colour=discord.Color.teal(), description=text)
        await interaction.response.send_message(embed=embed)


#ALIAS COMMANDS - PUBLIC USE
class alias(app_commands.Group):
    #Add alias
    @app_commands.command()
    @app_commands.describe(name='Name of the player', alias='Alias to add')
    async def add(self, interaction: discord.Interaction, alias: str, name: str):
        database.add_alias_to_db(name, alias)

        await interaction.response.send_message('Added alias {} for player {}.'.format(alias, name))

    #list all aliases
    @app_commands.command()
    async def list(self, interaction: discord.Interaction):
        aliases = database.get_aliases()
        text = "**Aliases:**\n"
        for alias, name in aliases.items():
            text += "{}-> {}\n".format(alias, name)
        embed = discord.Embed(colour=discord.Color.teal(), description=text)
        await interaction.response.send_message(embed=embed)

class votecount(app_commands.Group):
    #get retrospective votecount
    @app_commands.command()
    @app_commands.describe(game='Available Games', postnum="Post Number")
    async def get_retrospective(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C'], postnum: int):
        #check if channel name is votecount-game-X
        if interaction.channel.name == "votecount-game-{}".format(game):
            votecount = get_votecount(game, postnum)
            embed = discord.Embed(colour=discord.Color.orange(), description=votecount.replace("_",""))
            await interaction.response.send_message(embed=embed)
        else:
            #send an ephemeral message
            await interaction.response.send_message("Please use this command in the right channel!", ephemeral=True)

    #get current votecount
    @app_commands.command()
    @app_commands.describe(game='Available Games')
    async def get_current(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C']):
        if interaction.channel.name == "votecount-game-{}".format(game):
            votecount = get_votecount(game, float('inf'))
            embed = discord.Embed(colour=discord.Color.green(), description=votecount.replace("_",""))
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Please use this command in the right channel!", ephemeral=True) 

    #list all aliases
    @app_commands.command()
    async def list(self, interaction: discord.Interaction):
        aliases = database.get_aliases()
        text = "**Aliases:**\n"
        for alias, name in aliases.items():
            text += "{}-> {}\n".format(alias, name)
        embed = discord.Embed(colour=discord.Color.teal(), description=text)
        await interaction.response.send_message(embed=embed)

#ISO COMMANDS - PUBLIC USE
class rank_activity(app_commands.Group):
    #rank activity
    @app_commands.command()
    @app_commands.describe(game='Available Games')
    async def all(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C']):
        if interaction.channel.name != "iso-bot":
            await interaction.response.send_message("Please use this command in the iso-bot channel!", ephemeral=True)
        else:
            ranking = database.get_authors(game, 1, float('inf'))
            text = "**Activity ranking for game {}:**\n".format(game)
            for row in ranking:
                text += "{}: {}\n".format(row["_id"], row["count"])
            embed = discord.Embed(colour=discord.Color.teal(), description=text.replace("_",""))
            await interaction.response.send_message(embed=embed)

    #rank activity today
    @app_commands.command()
    @app_commands.describe(game='Available Games')
    async def today(self, interaction: discord.Interaction, game: Literal['A', 'B', 'C']):
        if interaction.channel.name != "iso-bot":
            await interaction.response.send_message("Please use this command in the iso-bot channel!", ephemeral=True)
        else:
            phase = database.get_phases(game)[-1]
            ranking = database.get_authors(game, phase['postnum'], float('inf'))
            text = "**{} activity ranking for game {}:**\n".format(phase['phase'], game)
            for row in ranking:
                text += "{}: {}\n".format(row["_id"], row["count"])
            embed = discord.Embed(colour=discord.Color.teal(), description=text.replace("_",""))

            await interaction.response.send_message(embed=embed) 


#SPECIAL COMMANDS - PUBLIC USE
class special(app_commands.Group):
    #help command
    @app_commands.command()
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=help_message)

    #ping command
    @app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Still here!")

    #give link to web interface
    @app_commands.command()
    async def web(self, interaction: discord.Interaction):
        await interaction.response.send_message("Web interface: {}".format('WIP'))
