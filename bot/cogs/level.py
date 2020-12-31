from discord import Message
from discord.ext import commands
from bot.util.level_calculator import LevelCalculator
from bot import Bot


class Level(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def message(self, msg: Message):
        if msg.guild:
            history = await msg.channel.history(limit=10).flatten()

            LevelCalculator.calculate_text_xp(msg, history)
            LevelCalculator.calculate_next_level(1)


def setup(bot: Bot):
    bot.add_cog(Level(bot))