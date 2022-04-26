# Description
An easy-to-use cloud database that uses a GitHub repository to store data.
# Example
Using an example, I will show you how to create a database for a Discord server using pycord
```py
import discord
from discord.ext import commands,tasks
import os, sys, json
from github import Github
import asyncio
from settings.dbkirosake import DBKirosake
from settings.config import *

DB=DBKirosake(
    actoken,
    repos
)

intents = discord.Intents.all()

client = commands.Bot(
    command_prefix=prefix,
    intents=intents,
    bot=True
)
client.remove_command('help')

@client.event
async def on_ready():
    for guild in client.guilds:
        for member in guild.members:
            db={
                'lvl':1,
                'cash':10
            }
            await DB.create_db(
                nameDB='test',
                folder=guild.id,
                ids=member.id,
                database=db
            )
    
client.run(token)
```
