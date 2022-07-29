from app.model import AlertSchema, UserSchema, LoginSchema
from fastapi import FastAPI, Body, Depends
from app.auth.auth_handler import signJWT
from app.auth.bearer import JWTBearer
from app.auth.security import verify_password, hash_password

alerts = [
        {
            "id": 1,
            "status": "created",
            "targetPrice": 24000.78
        }
]

users = []
app = FastAPI()

@app.get("/", tags=["Welcome"])
async def home() -> dict:
    return {"message": "Welcome to your crypto-assistant!"}

@app.post("/alerts/create", dependencies=[Depends(JWTBearer())], tags=["Create Alerts"])
async def add_alert(alert: AlertSchema) -> dict:
    alert.alert_id = len(alerts) + 1
    alerts.append(alert.dict()) # replace with db call
    return {"data": "New Alert has been added"}

@app.get("/alerts/fetch", tdependencies=[Depends(JWTBearer())], tags=["Fetch Alerts"])
async def fetch_alerts() -> dict:
    return {"data": alerts}

# For debugging and such, will delete later
@app.get("/user/fetch", tags=["Fetch All Users"])
async def fetch_users() -> dict:
    return {"users": users}

@app.post("/user/signup", tags=["User Signup"])
async def create_user(user: UserSchema):
    if not check_user(user):
        user.password = hash_password(user.password)  
        users.append(user) # replace with db call, making sure to hash password
        return signJWT(user.email)
    return {"error": "User Exists!"} 

@app.post("/user/login", tags=["User Login"])
async def user_login(user: LoginSchema = Body(...)):
    # here you must hash the password
    if check_user(user):
        user.password = hash_password(user.password)  
        return signJWT(user.email)
    return {"error": "Wrong User Credentials!"} 

'''Helper Functions'''
def check_user(data: LoginSchema):
    for user in users:
        if user.email == data.email and verify_password(data.password, user.password):
            return True
    return False
