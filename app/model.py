from pydantic import BaseModel, Field, EmailStr

class AlertSchema(BaseModel):
    alert_id: str = Field(default="", title="Unique ID")
    status: str = Field(default="", title="The status of the alert: created/deleted/triggered")
    targetPrice: int = Field(gt=0, title="The target price at which the alert will get triggered")
    email: EmailStr 
    class Config:
        schema_extra = {
                "example": {
                    "status": "created",
                    "targetPrice": 24000,
                    "email": "arjunsomvanshi@gmail.com"
                    }
                }

class UserSchema(BaseModel):
    username: str
    email: EmailStr 
    password: str 
    alerts: list
    class Config:
        schema_extra = {
            "example": {
                "username": "Arjun Somvanshi",
                "email": "arjunsomvanshi@gmail.com",
                "password": "usuallyStrongPassword",
                "alerts": []
            }
        }

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    class Config:
        schema_extra = {
            "example": {
                "email": "arjunsomvanshi@gmail.com",
                "password": "usuallyStrongPassword"
            }
        }
    
