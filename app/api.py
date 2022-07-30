from app.model import AlertSchema, UserSchema, LoginSchema, EmailStr
from fastapi import FastAPI, Body, Depends
from app.auth.auth_handler import signJWT
from app.auth.bearer import JWTBearer
from app.auth.security import verify_password, hash_password
from app.database import db, check_user, get_user, get_alert, update_user, update_alert, generate_alert_id

users = [] # list of existing users
alerts = [] # mapped from id -> alert object
app = FastAPI()

@app.get("/", tags=["Welcome to something"])
async def home() -> dict:
    return {"message": "Welcome to your crypto-assistant!"}

@app.post("/alerts/create", dependencies=[Depends(JWTBearer())], tags=["Create Alert"])
async def add_alert(user: UserSchema, alert: AlertSchema) -> dict:
    # replace with db call
    alert.status = "created"
    alert.alert_id = generate_alert_id()
    # add the alert in users alert list
    user.alerts.append(alert.dict()) 
    update_user(user)
    # inserting in database
    alertCollection = db["alerts"]
    alert_id = alertCollection.insert_one(alert.dict()).inserted_id
    return {"data": "New Alert has been added"}

@app.post("/alerts/delete", dependencies=[Depends(JWTBearer())], tags=["Delete Alert"])
async def delete_alert(user: UserSchema, targetAlert: AlertSchema) -> dict:
    update_alert(targetAlert, {"$set": {"status": "deleted"}})
    for alert in user.alerts:
        if alert["alert_id"] == targetAlert.alert_id:
            alert["status"] = "deleted"
            break
    update_user(user)
    return {"data": str(targetAlert) + " has been deleted"}

@app.get("/alerts/fetch", dependencies=[Depends(JWTBearer())], tags=["Fetch Alerts"])
async def fetch_alerts(email: EmailStr, filterStr: str = None) -> dict:
    alertCollection = db["alerts"]
    result = []
    if filterStr in ["created", "triggered", "deleted"]:
        query = {"email": email, "status": filterStr}
    else:
        query = {"email": email}
    for alert in alertCollection.find(query):
        del alert["_id"]
        result.append(alert)
    return {"user": result}

# For debugging and such, will delete later REMOVE ME (the function)
@app.get("/user/fetch", tags=["Fetch User by EmailID"])
async def fetch_user(email: EmailStr) -> dict:
    userCollection = db["users"]
    u = userCollection.find_one({"email": email})
    return {"user": str(u)}

@app.post("/user/signup", tags=["User Signup"])
async def create_user(user: UserSchema):
    if not check_user(user, signup = True):
        user.password = hash_password(user.password)  
        # database calls 
        userCollection = db["users"]
        userCollection.insert_one(user.dict()).inserted_id
        return signJWT(user.email)
    return {"error": "User Exists!"} 

@app.post("/user/login", tags=["User Login"])
async def user_login(user: LoginSchema = Body(...)):
    # here you must hash the password
    if check_user(user):
        user.password = hash_password(user.password)  # getting rid of plain text idk if it's need :p but can't be wrong
        return signJWT(user.email)
    return {"error": "Wrong User Credentials!"} 

