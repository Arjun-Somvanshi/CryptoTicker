# connect with database
from pymongo import MongoClient
import os
client = MongoClient('mongodb://mongodb:27017',
                     username='arjun',
                     password='arjun1234')
db = client.cryptoTicker
