# connect with database
from app.model import AlertSchema, UserSchema, LoginSchema, EmailStr
from pymongo import MongoClient
from app.auth.security import verify_password, hash_password
import string
import random
import os
client = MongoClient('mongodb://mongodb:27017',
                     username='arjun',
                     password='arjun1234')
db = client.cryptoTicker

'''Helper Functions'''
def check_user(data: LoginSchema, signup = False):
    userCollection = db["users"]
    u = userCollection.find_one({'email': data.email})
    if u != None:
        if verify_password(data.password, u['password']):
            return True
        if signup:
            return True
    return False

def get_user(user: UserSchema):
    userCollection = db["users"]
    u = userCollection.find_one({'email': user.email})
    if verify_password(user.password, u['password']):
        return u

def get_alert(alert: AlertSchema):
    alertCollection = db["alerts"]
    a = alertCollection.find_one({"alert_id": alert.alert_id})
    return a

def update_user(user: UserSchema):
        u = get_user(user)
        newValues = {"$set": {"alerts": user.alerts}}
        db["users"].update_one(u, newValues) 

def update_alert(alert: AlertSchema, newValues):
        a = get_alert(alert)
        db["alerts"].update_one(a, newValues) 

def generate_alert_id():
    N = 8
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    return str(res) 
