import discord
from discord.ext import commands
import json
import datetime
import re

with open('Percorso specificato (usate il \)', 'r') as settings:     
    options = json.load(settings)

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print(f"SwapiTeams Automoderation Bot, activated! Loggato come: {client.user}. Ore: {datetime.datetime.utcnow()}. Contact SwapiTeams for support: https://discord.gg/CJ8t5sgBaA. Versione: {options['version']}")
    if options['automod'] == True:
        print(f"Caricato il settings.json | Automod: Attivato")
    elif options['automod'] == False:
        print(f"Caricato il settings.json | Automod: Disattivato")
    else:
        print("Non sono riuscito a caricare il settings.json")

def msg_cont(message, word):
    return re.search(fr'\b({word})\b', message) is not None

@client.event
async def on_message(message):
    bannedwords = options['bannedwords']
    if options['automod'] == True:
        if bannedwords != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
            for bannedword in bannedwords:
                if msg_cont(message.content.lower(), bannedword):
                    await message.delete()

                    embed = discord.Embed(
                        title="Automod",
                        description=f"{message.author} non puoi scrivere questa parola",
                        color=0x1d1d1d
                    )

                    await message.channel.send(embed=embed)

                    print(f"{message.author} ha scritto {message.content} in {message.channel}")

            await client.process_commands(message)

client.run(f"{options['token']}")