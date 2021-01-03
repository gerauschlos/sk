from gino import Gino

db = Gino()


class ServerModel(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.BigInteger(), primary_key=True)
    prefix = db.Column(db.Text())

    def __repr__(self):
        return f'Server({self.id=}, {self.prefix=})'


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BigInteger())
    server_id = db.Column(db.BigInteger(), db.ForeignKey("servers.id"))
    level = db.Column(db.Integer())
    voice_xp = db.Column(db.BigInteger())
    text_xp = db.Column(db.BigInteger())
    last_message_ts = db.Column(db.BigInteger())  # timestamp of last message sent

    _guild_user_uniq = db.UniqueConstraint('user_id', 'server_id', name="server_user")

    def __repr__(self):
        return f'User({self.user_id=}, {self.level=}, {self.server_id=}, {self.voice_xp=}, {self.text_xp=}, {self.last_message_ts=})'


async def bind_database(postgres_login: str):
    await db.set_bind(postgres_login)
    await db.gino.create_all()
