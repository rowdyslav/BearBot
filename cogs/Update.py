import requests
import asyncio
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
        print(guilds)
        voice_channels = [channel for guild in guilds
                          for channel in guild.voice_channels
                          if channel.name.startswith('BEAR token')]
        response = requests.get(self.api)
        if response.status_code == 200:
            value = response.json()['data']['value']
            print(value)
        else:
            print('Произошла ошибка при запросе к API')
            return
        print(voice_channels)
        for channel in voice_channels:
            print(f'Название канала {channel.name}, сервер {channel.guild}')
            await channel.edit(name=f'BEAR token: ${str(value)[:5]}')
            print(f'Канал на сервере {channel.guild} обновлен!')
        await asyncio.sleep(3)

    @update_channels.before_loop
    async def before_update_channels(self):
        print('Ожидание запуска задачи...')
        await self.client.wait_until_ready()


async def setup(client):
    await client.add_cog(Update(client))
