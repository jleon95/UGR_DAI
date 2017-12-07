from django.db import models
import pymongo as pym

client = pym.MongoClient()
collection = client.database.restaurants
