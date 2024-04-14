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


class Weight(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    weight = DecimalField(default=1)

    class Meta:
        db_table = 'weights'


class Vote(BaseModel):
    id = PrimaryKeyField()
    option_id = ForeignKeyField(Option, backref='votes')
    weight_id = ForeignKeyField(Weight, backref='votes')
    datetime = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'votes'
