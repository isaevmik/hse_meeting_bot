from database.database_configuration import db
import peewee
from uuid import uuid4


class BaseModel(peewee.Model):
    class Meta:
        database = db


class bot_users(BaseModel):
    uuid = peewee.UUIDField(primary_key=True, default=uuid4)
    telegram_id = peewee.BigIntegerField(null=False, unique=True)
    chat_id = peewee.BigIntegerField(null=False, unique=True)
    first_name = peewee.TextField(null=False)
    last_name = peewee.TextField(null=True)
    tg_username = peewee.TextField(null=True)
    status = peewee.TextField(null=False, default="INACTIVE")

    class Meta:
        database = db


class meetings(BaseModel):
    uuid = peewee.UUIDField(primary_key=True, default=uuid4)
    telegram_id_1 = peewee.ForeignKeyField(bot_users, to_field="chat_id")
    chat_id_1 = peewee.ForeignKeyField(bot_users, to_field="telegram_id")
    telegram_id_2 = peewee.ForeignKeyField(bot_users, to_field="chat_id")
    chat_id_2 = peewee.ForeignKeyField(bot_users, to_field="telegram_id")
    status = peewee.TextField(null=False, default="ACTIVE")

    class Meta:
        database = db
