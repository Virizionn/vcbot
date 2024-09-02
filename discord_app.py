from typing import Literal

import discord
from discord import app_commands

import json

import database

async def updateStatus(status):
  game = discord.Game(status)
  await client.change_presence(status=discord.Status.online, activity=game)
  print("Updated status to {}".format(status))
  return

def is_host(interaction: discord.Interaction) -> bool:
  for role in interaction.user.roles:
    if (role.name in ["Mafia", "Puppeteer (Host)", "God"]):
      print("Passed check.")
      return True
  print("FAILED check.")
  return False

intents = discord.Intents.default()
intents.message_content = True
test_guild = discord.Object(id="951678432494911528")
help_message = discord.Embed(colour=discord.Color.teal(),
                             description="""WIP""")


client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command()
@app_commands.check(is_host)
@app_commands.describe(game='Available Games', url="game url")
async def url(interaction: discord.Interaction, game: Literal['A', 'B', 'C'], url: str):
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
    database.set_url(game, url)

    await interaction.response.send_message(
        'Wiped post database and Set url for game {} to {}.'.format(game, url))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#message event - check if a message is equal to #sync
@client.event
async def on_message(message):
   if message.text == "$sync":
        #global sync discord command tree
        tree.sync()
        await message.channel.send("Global synced command tree.")


#read discord token from Credentials/discord_secret.json
with open("Credentials/discord_secret.json") as f:
    data = json.load(f)
    token = data["token"]

client.run(token)


