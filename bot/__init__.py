from typing import List
from discord import Guild, Message
from discord.ext import commands
from discord.ext.commands import CheckFailure, Context
from .models import bind_database, ServerModel
import yaml
import os

INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id={}&permissions=0&scope=bot'
DEFAULT_PREFIX = "+"


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_extensions()

        self.prefixes = {}

    def load_extensions(self):
        file_names = [f[:-3] for f in os.listdir('./bot/cogs') if f.endswith('.py')]

        for file_name in file_names:
            self.load_extension(f'bot.cogs.{file_name}')

    @staticmethod
    def get_postgres_login():
        with open("config.yaml") as f:
            postgres_login = yaml.load(f, Loader=yaml.FullLoader)["postgres_login"]

        return postgres_login

    async def load_prefixes(self):
        for guild in self.guilds:
            if server := await ServerModel.get(guild.id):
                self.prefixes[guild.id] = server.prefix
            else:
                await ServerModel.create(id=guild.id)

    async def on_ready(self):
        await bind_database(self.get_postgres_login())
        await self.load_prefixes()

        print(
            f"""Logged in as {self.user}...
With {len(self.users)} users in {len(self.guilds)} servers
Invite Link: {INVITE_LINK.format(self.user.id)}
            """
        )

    @staticmethod
    async def on_guild_join(guild: Guild):
        if not (await ServerModel.get(guild.id)):
            await ServerModel.create(id=guild.id)

    async def on_command_error(self, ctx: Context, error: CheckFailure):
        print("it worked")


def get_prefix(bot: Bot, msg: Message) -> List[str]:
    prefix = bot.prefixes.get(msg.guild.id, DEFAULT_PREFIX)

    return commands.when_mentioned_or(prefix)(bot, msg)


bot = Bot(command_prefix=get_prefix)
