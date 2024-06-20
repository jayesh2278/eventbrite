import peewee
from peewee import *


db = MySQLDatabase('company_info', host="localhost", user="root", password="Pizzatime730")

class Eventbrite(peewee.Model):
    title = peewee.CharField()
    image = peewee.CharField(null=True)
    event_url = peewee.CharField()
    date_time = peewee.CharField(null=True)
    location = peewee.CharField(null=True)
    tags = peewee.CharField(null=True)
    all_text = peewee.TextField()

    class Meta:
        database = db
        db_table='Eventbrite'
    
