import requests
from discord.ext import commands, tasks
from icecream import ic


class Madbeartoken(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api = 'https://public-api.birdeye.so/public/price?address\
=Ee1pKgTQmP5xjYQs76HmRM2c2YkqEdc9tk5mQbiGFigT'
        self.headers = {"X-API-KEY": "9a3d1efa360344c19319da060e7dfefb"}
        self.update_channels.start()

    def cog_unload(self):
        self.update_channels.cancel()

    @tasks.loop(minutes=10)
    async def update_channels(self):
        guilds = self.client.guilds
        voice_channels = [channel for guild in guilds
                          for channel in guild.voice_channels
                          if channel.name.startswith('Price')]
        response = requests.get(self.api, headers=self.headers)
        if response.status_code == 200:
            value = response.json()['data']['value']
        else:
            ic('Произошла ошибка при запросе к API')
            return
        for channel in voice_channels:
            await channel.edit(name=f'Price: ${str(value)[:5]}')
            ic(f'Канал на сервере {channel.guild} обновлен!')

    @update_channels.before_loop
    async def before_update_channels(self):
        await self.client.wait_until_ready()


async def setup(client):
    await client.add_cog(Madbeartoken(client))
