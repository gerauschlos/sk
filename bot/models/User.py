from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BigInteger())
    guild_id = db.Column(db.BigInteger(), db.ForeignKey("guilds.id"))
    voice_xp = db.Column(db.BigInteger())
    text_xp = db.Column(db.BigInteger())

    _guild_user_uniq = db.UniqueContraint('user_id', 'guild_id', name="guild_user")
