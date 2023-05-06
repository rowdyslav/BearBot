import requests
from discord.ext import commands, tasks
# import discord


class Update(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api = 'https://public-api.birdeye.so/public/price?address\
=9LmCL3nyvFG95cB9RpaszPTAwaQykVAHcSxQbJ6vNpAU'
        self.update_channels.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('update работает!')

    def cog_unload(self):
        self.update_channels.cancel()  # отменяем задачу при выгрузке Cog

    @tasks.loop(minutes=10)
    async def update_channels(self):
        guilds = self.client.guilds  # получаем первую гильдию бота
        voice_channels = [channel for guild in guilds
                          for channel in guild.voice_channels
                          if channel.name.startswith('BEAR token')]
        response = requests.get(self.api)
        if response.status_code == 200:
            value = round(response.json()['data']['value'], 3)
        else:
            print('Произошла ошибка при запросе к API')
            return
        for channel in voice_channels:
            await channel.edit(name=f'BEAR token: ${value}')
            print(f'Канал на сервере {channel.guild} обновлен!')

    @update_channels.before_loop
    async def before_update_channels(self):
        print('Ожидание запуска задачи...')
        await self.client.wait_until_ready()


async def setup(client):
    await client.add_cog(Update(client))
