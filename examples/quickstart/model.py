from peewee import *
import config

db = SqliteDatabase('people.db')

class Person(Model):
    firstname = CharField()
    surname = CharField()

    class Meta:
        database = db

if __name__ == "__main__":
    db.connect()
    db.create_tables([Person])

    # Add some data
    Person(firstname="John", surname="Bob").save()
    Person(firstname="Jane", surname="Bob").save()
    Person(firstname="Michael", surname="Clark").save()
