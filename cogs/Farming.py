import requests
from discord.ext import commands, tasks
from icecream import ic


def json_find(verst, key, value):
    for dict_index in range(len(verst)):
        if verst[dict_index][key] == value:
            return dict_index


class Farmingpoolsecond(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.apis = ['https://api.raydium.io/v2/main/pairs',
                     'https://api.raydium.io/v2/main/farm/info']
        self.update_channels.start()

    def cog_unload(self):
        self.update_channels.cancel()

    @tasks.loop(minutes=60)
    async def update_channels(self):
        guilds = self.client.guilds
        voice_channels = [channel for guild in guilds
                          for channel in guild.voice_channels
                          if channel.name.startswith('Farming APR')]
        first_r = requests.get(self.apis[0])
        if first_r.status_code == 200:
            first = first_r.json()[json_find(first_r.json(), "ammId", "6wnz14fhCZzMsBVG7ooB5eP3aPNkhEMrJ5FrqRFt8xF4")][
                'apr24h']
        else:
            ic('Произошла ошибка при запросе к API')
            return
        second_r = requests.get(self.apis[1])
        if second_r.status_code == 200:
            second = float(second_r.json()['data'][json_find(second_r.json()["data"], "id",
                                                             "Bq6QumT1mVBn2b1DCxNDRfZ171J7mX8rH5aYTyRYLddY")]['apr'][
                           :-1])
        else:
            ic('Произошла ошибка при запросе к API')
            return
        for channel in voice_channels:
            await channel.edit(
                name=f'Farming APR: {str(round(first + second, 1))}%'
            )
            ic(f'Канал на сервере {channel.guild} обновлен!')

    @update_channels.before_loop
    async def before_update_channels(self):
        await self.client.wait_until_ready()


async def setup(client):
    await client.add_cog(Farmingpoolsecond(client))
