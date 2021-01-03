from datetime import datetime
from discord import Message, Member, Guild, TextChannel
from discord.ext import commands
from discord.ext.commands import CheckFailure, Context
from bot import Bot
from bot.models import UserModel


class Level(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def update_level(author: Member, guild: Guild):
        user: UserModel = await UserModel.query.where(UserModel.user_id == author.id and UserModel.guild_id == guild.id).gino.first()
        total_xp: int = user.text_xp + user.voice_xp
        next_level = user.level + 1
        xp_needed = 250 * (next_level ^ 2) - (250 * next_level)

        if xp_needed < total_xp:
            await user.update(level=next_level)

    @staticmethod
    async def add_text_xp(msg: Message):
        author: Member = msg.author
        guild: Guild = msg.guild
        channel: TextChannel = msg.channel
        user: UserModel = await UserModel.query.where(UserModel.user_id == author.id and UserModel.guild_id == guild.id).gino.first()

        dt = int(datetime.utcnow().timestamp())

        if user:
            seconds_passed = dt - user.last_message_ts
            if 60 > seconds_passed:
                messages = 0
                async for message in channel.history(after=user.last_message_ts, limit=None):
                    if message.author.id == author.id:
                        messages += 1

                if messages >= 30:
                    xp = 150
                else:
                    xp = 50 + int(200 * messages/seconds_passed)

                await user.update(text_xp=user.text_xp+xp)
        else:
            await UserModel.create(user_id=author.id, server_id=guild.id, last_message_ts=dt)

    @staticmethod
    async def add_voice_xp(author: Member, guild: Guild):
        pass

    @commands.Cog.listener()
    async def message(self, msg: Message):
        if msg.guild and not msg.author.bot:
            await self.add_text_xp(msg)
            await self.update_level(msg.author, msg.guild)

    @staticmethod
    async def on_command_error(ctx: Context, error: CheckFailure):
        raise


def setup(bot: Bot):
    bot.add_cog(Level(bot))