import requests
from discord.ext import commands
# import discord


class Create(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api = 'https://public-api.birdeye.so/public/price?address\
=9LmCL3nyvFG95cB9RpaszPTAwaQykVAHcSxQbJ6vNpAU'

    @commands.Cog.listener()
    async def on_ready(self):
        print('Команда create работает!')

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def create(self, ctx):
        response = requests.get(self.api)
        if response.status_code == 200:
            value = response.json()['data']['value']
        else:
            ctx.send('Произошла ошибка при запросе к API')
        await ctx.guild.create_voice_channel(f'BEAR token: ${round(value, 9)}')


async def setup(client):
    await client.add_cog(Create(client))
