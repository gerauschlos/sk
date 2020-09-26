from . import db


class Guild(db.Model):
    __tablename__ = "guilds"

    id = db.Column(db.BigInteger(), primary_key=True)
    prefix = db.Column(db.Text())
