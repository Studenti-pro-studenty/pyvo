from peewee import *
import datetime

DATABASE_PATH = '../pyvo.db'
DATABASE = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = DATABASE


class Info(BaseModel):
    key = TextField(primary_key=True)
    value = TextField()

    class Meta:
        db_table = 'info'


class Option(BaseModel):
    id = PrimaryKeyField()
    name = TextField()

    class Meta:
        db_table = 'options'


class Vote(BaseModel):
    id = PrimaryKeyField()
    option_id = ForeignKeyField(Option, backref='votes')
    count = DecimalField(default=0)
    datetime = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'votes'
