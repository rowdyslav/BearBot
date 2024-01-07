import os
import asyncio
from uptimerobot import keep_alive
import discord
from discord.ext import commands

token = os.environ['BearBot']

client = commands.Bot(command_prefix='!!', intents=discord.Intents.all())


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Ког {filename[:-3]} загружен!')


async def main():
    async with client:
        await load()
        keep_alive()
        await client.start(token)


@client.event
async def on_ready():
    await client.change_presence()
    print('Бот работает!')


asyncio.run(main())

# https://discord.com/api/oauth2/authorize?client_id=1104397332151279689&permissions=8&scope=bot
