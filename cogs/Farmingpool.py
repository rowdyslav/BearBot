import requests
from discord.ext import commands, tasks
# import discord


def json_find(verst, key, value):
    for dict_index in range(len(verst)):
        if verst[dict_index][key] == value:
            return dict_index


class Farmingpool(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.apis = ['https://api.raydium.io/v2/main/pairs',
                     'https://api.raydium.io/v2/main/farm/info']
        self.update_channels.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('update работает!')

    def cog_unload(self):
        self.update_channels.cancel()  # отменяем задачу при выгрузке Cog

    @tasks.loop(minutes=60)
    async def update_channels(self):
        guilds = self.client.guilds
        voice_channels = [channel for guild in guilds
                          for channel in guild.voice_channels
                          if channel.name.startswith('Farming APR')]
        first_r = requests.get(self.apis[0])
        first_r = requests.get(self.apis[0])
        if first_r.status_code == 200:
            first = first_r.json()[json_find(first_r.json(), "ammId", "GvRj43J4Mk93rmS8VFPVHEHDafrUwmbH625RgpPafZjQ")]['apr24h']
            print(first)
        else:
            print('Произошла ошибка при запросе к API')
            return
        second_r = requests.get(self.apis[1])
        if second_r.status_code == 200:
            second = float(second_r.json()['data'][json_find(second_r.json()["data"], "id", "HP7Pg9MJ6HhRWJRPryxCZ1ziXr7H8qFWBQrcuLQUrLp3")]['apr'][:-1])
            print(second)
        else:
            print('Произошла ошибка при запросе к API')
            return
        for channel in voice_channels:
            print(f'Название канала {channel.name}, сервер {channel.guild}')
            await channel.edit(
                name=f'Farming APR: {str(round(first + second, 1))}%'
                )
            print(f'Канал на сервере {channel.guild} обновлен!')

    @update_channels.before_loop
    async def before_update_channels(self):
        print('Ожидание запуска задачи...')
        await self.client.wait_until_ready()


async def setup(client):
    await client.add_cog(Farmingpool(client))
